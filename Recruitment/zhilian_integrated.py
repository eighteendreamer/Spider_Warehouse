"""
智联招聘爬虫 - 整合版
整合列表爬取和详情爬取功能
"""

import requests
import json
import time
import random
import csv
from curl_cffi import requests as cffi_requests
from lxml import etree


class ZhilianCrawler:
    """智联招聘爬虫"""
    
    def __init__(self):
        # 列表API的headers
        self.list_headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://www.zhaopin.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.zhaopin.com/",
            "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "x-zp-business-system": "1",
            "x-zp-page-code": "4019",
            "x-zp-platform": "13"
        }
        
        # 列表API的cookies（需要定期更新）
        self.list_cookies = {
            "x-zp-client-id": "30023de0-d1b2-4738-a518-a1621627d26c",
            "sajssdk_2015_cross_new_user": "1",
            "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%2219dee8d2fc5560-01779b6d1278a92-26061e51-1327104-19dee8d2fc611d9%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTlkZWU4ZDJmYzU1NjAtMDE3NzliNmQxMjc4YTkyLTI2MDYxZTUxLTEzMjcxMDQtMTlkZWU4ZDJmYzYxMWQ5In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219dee8d2fc5560-01779b6d1278a92-26061e51-1327104-19dee8d2fc611d9%22%7D",
            "sensorsdata2015jssdkchannel": "%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D",
            "Hm_lvt_7fa4effa4233f03d11c7e2c710749600": "1777823725",
            "HMACCOUNT": "6DC40D2860C660F6",
            "x-zp-device-sn": "7efde1ac846b4fa59882fdd4aa65ce55",
            "Hm_lpvt_7fa4effa4233f03d11c7e2c710749600": "1777823743",
            "locationInfo_search": "{%22code%22:%22551%22,%22name%22:%22%E9%87%8D%E5%BA%86%22,%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}",
            "LastCity": "%E9%87%8D%E5%BA%86",
            "LastCity%5Fid": "551",
            "selectCity_search": "489"
        }
        
        # 列表API的URL参数（需要定期更新）
        self.list_params = {
            "MmEwMD": "5fdstlGZy9a17K2JJ1NndxEOZiJTGUkoKOpDenmlUFCOF_5NFfjiw3i9MGW3OfnMu20avGrXuWmtZPu9iWtjUVs_w4eXQxq79dgvseCRczhqMHWWHHkYoU8_SqlNSmpn8jgVWh9jIO823.woN2v5xWfAIuE89SlrauD4S.MMQWjdz.SgQxbm4Rgz.T9hZICfE9jZLETMfVLEkxLHQ55yqW3on5gTinL9L6rhHsillOrLQY.jc9Uw82SUQ92V6MWPDooZbmTxhk4X0D_6Ig7Jo.w8rIq.ryzd34JyGXo4LZFubV9cPcjzSHzKARRiR1PSmDCQ56o9nIWrXSwwnAHaMTuX2qrTzh4I5nayawYf3JGXkMz7m7nA8bjbA2q0hdZrWOJ.XrgOAr3XHZHIa2Ia7ta",
            "c1K5tw0w6_": "4FPw5rHeK1wuowfC380ApYTj.LiCNqqiyzl_RXM6KXYk5QXEBOX_2JWYvxo.Hr09E9SOsW8ko1p3DqofmcDEC05P_iIfG1XoDaSV.jekZRj8Tl_Goa_yCUjJCXSMtT2U1cf_kUJjtlve3OqD_c19kht7MdOpGtwO6MsvyI61saCdPvZOguBirDYpEnDUXSusmprXW_anCXll88_.Y3wCXT9D2kbTSo70V_44P3_ygFJD5MsbVxjggc1tI8N.Dl9nYY4t00ficprEuV2qGu64u3XbLiyX3W.0y2D3j864ZzWTihfhaho_3unIneb6j2aNL9AMO5AvBMASJ_npj8RcOwmbsFob31An.5s.9n9YWdjQ"
        }
        
        # 详情页的headers
        self.detail_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        
        self.list_url = "https://fe-api.zhaopin.com/c/i/search/positions"
        
    def get_job_list(self, keyword="人工智能", city_code="489", page_size=20, page_index=1):
        """
        获取职位列表
        
        Args:
            keyword: 搜索关键词
            city_code: 城市代码
            page_size: 每页数量
            page_index: 页码
            
        Returns:
            职位列表数据
        """
        data = {
            "S_SOU_WORK_CITY": city_code,
            "order": 4,
            "S_SOU_FULL_INDEX": keyword,
            "pageSize": page_size,
            "pageIndex": page_index,
            "eventScenario": "pcSearchedSouSearch",
            "anonymous": 1,
            "clickFilterBlackCompany": False,
            "platform": 13,
            "version": "0.0.0"
        }
        
        try:
            response = requests.post(
                self.list_url,
                headers=self.list_headers,
                cookies=self.list_cookies,
                params=self.list_params,
                data=json.dumps(data, separators=(',', ':')),
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                print(f"获取职位列表失败，状态码: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"获取职位列表异常: {e}")
            return None
    
    def get_job_detail(self, position_url):
        """
        获取职位详情页面
        
        Args:
            position_url: 职位详情URL
            
        Returns:
            HTML内容
        """
        try:
            # 使用curl_cffi模拟Chrome TLS指纹
            response = cffi_requests.get(
                position_url,
                headers=self.detail_headers,
                impersonate="chrome",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.text
            else:
                print(f"获取职位详情失败，状态码: {response.status_code}, URL: {position_url}")
                return None
                
        except Exception as e:
            print(f"获取职位详情异常: {e}, URL: {position_url}")
            return None
    
    def parse_job_detail(self, html_content):
        """
        解析职位详情页面，提取职责和能力要求
        
        Args:
            html_content: HTML内容
            
        Returns:
            dict: {"responsibilities": "职责", "requirements": "能力要求"}
        """
        if not html_content:
            return {"responsibilities": "", "requirements": ""}
        
        try:
            tree = etree.HTML(html_content)
            
            # 提取职位描述（包含职责和要求）
            # XPath: //div[@class='describtion-card__detail-content']
            desc_elements = tree.xpath('//div[contains(@class, "describtion-card__detail-content")]')
            
            if desc_elements:
                # 获取文本内容，保留<br>标签为换行
                desc_text = desc_elements[0].xpath('string(.)')
                
                # 简单分割职责和要求（根据常见关键词）
                # 这里可以根据实际情况调整分割逻辑
                responsibilities = ""
                requirements = ""
                
                # 尝试按常见关键词分割
                if "任职要求" in desc_text or "岗位要求" in desc_text or "职位要求" in desc_text:
                    parts = desc_text.split("任职要求")
                    if len(parts) == 1:
                        parts = desc_text.split("岗位要求")
                    if len(parts) == 1:
                        parts = desc_text.split("职位要求")
                    
                    if len(parts) >= 2:
                        responsibilities = parts[0].strip()
                        requirements = parts[1].strip()
                    else:
                        responsibilities = desc_text.strip()
                else:
                    # 如果没有明确分割，全部作为职责
                    responsibilities = desc_text.strip()
                
                return {
                    "responsibilities": responsibilities,
                    "requirements": requirements
                }
            else:
                print("未找到职位描述元素")
                return {"responsibilities": "", "requirements": ""}
                
        except Exception as e:
            print(f"解析职位详情异常: {e}")
            return {"responsibilities": "", "requirements": ""}
    
    def crawl(self, keyword="人工智能", city_code="489", max_pages=1, max_jobs=10):
        """
        爬取职位数据
        
        Args:
            keyword: 搜索关键词
            city_code: 城市代码
            max_pages: 最大爬取页数
            max_jobs: 最大爬取职位数
            
        Returns:
            职位数据列表
        """
        all_jobs = []
        job_count = 0
        
        for page in range(1, max_pages + 1):
            print(f"\n正在爬取第 {page} 页...")
            
            # 获取职位列表
            result = self.get_job_list(keyword, city_code, page_index=page)
            
            if not result:
                print("获取职位列表失败，停止爬取")
                break
            
            # 检查返回数据
            if result.get("code") != 200:
                print(f"API返回错误: {result}")
                break
            
            job_list = result.get("data", {}).get("list", [])
            
            if not job_list:
                print("没有更多职位数据")
                break
            
            print(f"获取到 {len(job_list)} 个职位")
            
            # 遍历职位列表
            for job in job_list:
                if job_count >= max_jobs:
                    print(f"\n已达到最大爬取数量 {max_jobs}，停止爬取")
                    return all_jobs
                
                print(f"\n{'='*60}")
                print(f"正在处理第 {job_count + 1} 个职位")
                print(f"{'='*60}")
                
                # 提取基本信息
                job_data = {
                    "求职网站": "智联招聘",
                    "公司名称": job.get("companyName", ""),
                    "岗位名": job.get("name", ""),
                    "需求数量": job.get("companySize", ""),
                    "职责": "",
                    "能力要求": "",
                    "薪资待遇": job.get("salary60", "")
                }
                
                print(f"公司名称: {job_data['公司名称']}")
                print(f"岗位名: {job_data['岗位名']}")
                print(f"薪资待遇: {job_data['薪资待遇']}")
                print(f"需求数量: {job_data['需求数量']}")
                
                # 获取职位详情URL
                position_url = job.get("positionURL") or job.get("positionUrl", "")
                
                if position_url:
                    print(f"职位详情URL: {position_url}")
                    
                    # 随机延迟，避免请求过快
                    delay = random.uniform(1, 3)
                    print(f"延迟 {delay:.2f} 秒...")
                    time.sleep(delay)
                    
                    # 获取详情页面
                    html_content = self.get_job_detail(position_url)
                    
                    if html_content:
                        # 解析详情
                        detail = self.parse_job_detail(html_content)
                        job_data["职责"] = detail["responsibilities"]
                        job_data["能力要求"] = detail["requirements"]
                        
                        print(f"\n职责内容 ({len(job_data['职责'])} 字符):")
                        print(job_data["职责"][:200] + "..." if len(job_data["职责"]) > 200 else job_data["职责"])
                        
                        print(f"\n能力要求 ({len(job_data['能力要求'])} 字符):")
                        print(job_data["能力要求"][:200] + "..." if len(job_data["能力要求"]) > 200 else job_data["能力要求"])
                    else:
                        print(f"❌ 获取详情失败")
                else:
                    print(f"❌ 职位URL为空")
                
                all_jobs.append(job_data)
                job_count += 1
                print(f"\n✅ 已成功爬取 {job_count}/{max_jobs} 个职位")
            
            # 页面间延迟
            if page < max_pages:
                delay = random.uniform(2, 4)
                print(f"\n页面间延迟 {delay:.2f} 秒...")
                time.sleep(delay)
        
        return all_jobs
    
    def save_to_json(self, jobs, filename="zhilian_jobs.json"):
        """
        保存数据到JSON文件
        
        Args:
            jobs: 职位数据列表
            filename: 文件名
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(jobs, f, ensure_ascii=False, indent=2)
            print(f"\n数据已保存到 {filename}")
        except Exception as e:
            print(f"保存JSON数据失败: {e}")
    
    def save_to_csv(self, jobs, filename="data/招聘.csv"):
        """
        保存数据到CSV文件（追加模式，不覆盖已有数据）
        
        Args:
            jobs: 职位数据列表
            filename: 文件名
        """
        if not jobs:
            print("没有数据可保存")
            return
        
        try:
            import os
            # 定义CSV列名
            fieldnames = ["求职网站", "公司名称", "岗位名", "需求数量", "职责", "能力要求", "薪资待遇"]
            
            file_exists = os.path.exists(filename)
            
            # 使用追加模式 'a'
            with open(filename, "a", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                # 如果文件不存在或为空，写入表头
                if not file_exists or os.path.getsize(filename) == 0:
                    writer.writeheader()
                
                writer.writerows(jobs)
            
            print(f"\n数据已追加到 {filename}，本次新增 {len(jobs)} 条记录")
        except Exception as e:
            print(f"保存CSV数据失败: {e}")
            import traceback
            traceback.print_exc()


def main():
    """主函数"""
    print("=" * 60)
    print("智联招聘爬虫 - 整合版")
    print("=" * 60)
    
    # 创建爬虫实例
    crawler = ZhilianCrawler()
    
    # 配置参数
    keyword = "人工智能"  # 搜索关键词
    city_code = "489"     # 城市代码（489=重庆）
    max_pages = 5         # 最大爬取页数
    max_jobs = 100          # 最大爬取职位数（测试用）
    
    print(f"\n搜索关键词: {keyword}")
    print(f"城市代码: {city_code}")
    print(f"最大页数: {max_pages}")
    print(f"最大职位数: {max_jobs}")
    
    # 开始爬取
    jobs = crawler.crawl(keyword, city_code, max_pages, max_jobs)
    
    # 保存数据
    if jobs:
        # 保存为CSV
        crawler.save_to_csv(jobs, "data/招聘.csv")
        # 打印完整数据
        print("\n" + "=" * 60)
        print("完整数据:")
        print("=" * 60)
        for idx, job in enumerate(jobs, 1):
            print(f"\n【职位 {idx}】")
            print(json.dumps(job, ensure_ascii=False, indent=2))
            print("-" * 60)
    else:
        print("\n未爬取到任何数据")


if __name__ == "__main__":
    main()
