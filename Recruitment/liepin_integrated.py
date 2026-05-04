import requests
import json
import time
from lxml import etree
import csv
from datetime import datetime


class LiepinSpider:
    def __init__(self):
        # 列表页headers
        self.list_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://www.liepin.com",
            "Referer": "https://www.liepin.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0",
            "X-Client-Type": "web",
            "X-Fscp-Bi-Stat": "{\"location\":\"https://www.liepin.com/zhaopin/?city=410&dq=410&pubTime=&currentPage=1&pageSize=40&key=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&suggestTag=&workYearCode=0&compId=&compName=&compTag=&industry=&salaryCode=&jobKind=&compScale=&compKind=&compStage=&eduLevel=&ckId=4cqx9p0vq6bfvm0fththre65rqrd5mfa&scene=page&skId=4cqx9p0vq6bfvm0fththre65rqrd5mfa&fkId=4cqx9p0vq6bfvm0fththre65rqrd5mfa&sfrom=search_job_pc&suggestId=\"}",
            "X-Fscp-Fe-Version;": "",
            "X-Fscp-Std-Info": "{\"client_id\": \"40108\"}",
            "X-Fscp-Trace-Id": "4a96774e-43f5-404a-8ce5-41c33ca4ea1b",
            "X-Fscp-Version": "1.1",
            "X-Requested-With": "XMLHttpRequest",
            "X-XSRF-TOKEN": "7BfUAFazTiiueFR-MvbgUA",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        
        # 详情页headers
        self.detail_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Referer": "https://www.liepin.com/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        
        self.cookies = {
            "__uuid": "1777828803813.97",
            "__sessionId": "1777828803816.33",
            "XSRF-TOKEN": "7BfUAFazTiiueFR-MvbgUA",
            "__gc_id": "2f2df64546b346ba9ff9e13d2412c5fb",
            "_uetsid": "5433f370471411f1a94429ad6b5a7258",
            "_uetvid": "54340940471411f1b556f353ead9d605",
            "_uetmsclkid": "_uet7ed24a1b3a921a4bd9b723ecb95344bf",
            "_clck": "1w6pqla%5E2%5Eg5q%5E0%5E2314",
            "_clsk": "2a8gvy%5E1777828809270%5E1%5E1%5El.clarity.ms%2Fcollect",
            "_ga": "GA1.1.625499567.1777828817",
            "Hm_lvt_a2647413544f5a04f00da7eee0d5e200": "1777828818",
            "HMACCOUNT": "04945B46930EF2FE",
            "acw_tc": "276077dc17778288185011580e453e001d05c281c842a33219528ae9816e08",
            "_ga_54YTJKWN86": "GS2.1.s1777828817$o1$g1$t1777828830$j47$l0$h0",
            "__session_seq": "5",
            "Hm_lpvt_a2647413544f5a04f00da7eee0d5e200": "1777828831",
            "__tlg_event_seq": "20"
        }
        
        self.list_url = "https://api-c.liepin.com/api/com.liepin.searchfront4c.pc-search-job"
    
    def get_job_list(self, keyword="人工智能", city="410", current_page=1, page_size=40):
        """获取职位列表"""
        data = {
            "data": {
                "mainSearchPcConditionForm": {
                    "city": city,
                    "dq": city,
                    "currentPage": current_page,
                    "pageSize": page_size,
                    "key": keyword,
                    "suggestTag": "",
                    "workYearCode": "0",
                    "compId": "",
                    "compName": "",
                    "compTag": "",
                    "industry": "",
                    "salaryCode": "",
                    "jobKind": "",
                    "compScale": "",
                    "compKind": "",
                    "compStage": "",
                    "eduLevel": "",
                    "salaryLow": "",
                    "salaryHigh": "",
                    "hrActiveTimeCode": ""
                },
                "passThroughForm": {
                    "ckId": "4jrkf7nlp1sjo91o8g4ujiyu4b3c1ad9",
                    "scene": "page",
                    "skId": "4cqx9p0vq6bfvm0fththre65rqrd5mfa",
                    "fkId": "4cqx9p0vq6bfvm0fththre65rqrd5mfa",
                    "sfrom": "search_job_pc"
                }
            }
        }
        
        data_str = json.dumps(data, separators=(',', ':'))
        
        try:
            response = requests.post(
                self.list_url, 
                headers=self.list_headers, 
                cookies=self.cookies, 
                data=data_str,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"获取职位列表失败: {e}")
            return None
    
    def get_job_detail(self, job_url):
        """获取职位详情"""
        try:
            response = requests.get(
                job_url, 
                headers=self.detail_headers, 
                cookies=self.cookies,
                timeout=10
            )
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            html = etree.HTML(response.text)
            
            # 提取职位介绍内容
            job_intro_element = html.xpath('//dd[@data-selector="job-intro-content"]')
            if job_intro_element:
                job_intro_text = job_intro_element[0].xpath('string(.)').strip()
                
                # 分割职位描述和任职要求
                responsibilities = ""
                requirements = ""
                
                if "任职要求" in job_intro_text:
                    parts = job_intro_text.split("任职要求")
                    responsibilities = parts[0].replace("职位描述", "").strip()
                    requirements = parts[1].strip() if len(parts) > 1 else ""
                else:
                    responsibilities = job_intro_text.replace("职位描述", "").strip()
                
                return {
                    "responsibilities": responsibilities,
                    "requirements": requirements
                }
            else:
                return {
                    "responsibilities": "",
                    "requirements": ""
                }
        except Exception as e:
            print(f"获取职位详情失败 {job_url}: {e}")
            return {
                "responsibilities": "",
                "requirements": ""
            }
    
    def parse_job_data(self, job_item, detail_info):
        """解析职位数据"""
        comp = job_item.get("comp", {})
        job = job_item.get("job", {})
        
        # 提取需求数量（从compScale中提取）
        comp_scale = comp.get("compScale", "")
        
        return {
            "求职网站": "猎聘",
            "公司名称": comp.get("compName", ""),
            "岗位名": job.get("title", ""),
            "需求数量": comp_scale,  # 公司规模作为需求数量
            "职责": detail_info.get("responsibilities", ""),
            "能力要求": detail_info.get("requirements", ""),
            "薪资待遇": job.get("salary", "")
        }
    
    def save_to_csv(self, data_list, filename="data/招聘.csv"):
        """保存数据到CSV（追加模式，不覆盖已有数据）"""
        if not data_list:
            print("没有数据可保存")
            return
        
        fieldnames = ["求职网站", "公司名称", "岗位名", "需求数量", "职责", "能力要求", "薪资待遇"]
        
        try:
            import os
            file_exists = os.path.exists(filename)
            
            # 使用追加模式 'a'
            with open(filename, mode='a', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                # 如果文件不存在或为空，写入表头
                if not file_exists or os.path.getsize(filename) == 0:
                    writer.writeheader()
                
                writer.writerows(data_list)
            
            print(f"数据已追加到 {filename}，本次新增 {len(data_list)} 条记录")
        except Exception as e:
            print(f"保存CSV失败: {e}")
    
    def run(self, keyword="人工智能", city="410", max_count=100):
        """运行爬虫"""
        all_data = []
        page = 1
        
        while len(all_data) < max_count:
            print(f"\n正在爬取第 {page} 页... (已获取 {len(all_data)}/{max_count} 条)")
            
            # 获取职位列表
            result = self.get_job_list(keyword=keyword, city=city, current_page=page)
            
            if not result or result.get("flag") != 1:
                print(f"第 {page} 页获取失败")
                break
            
            job_list = result.get("data", {}).get("data", {}).get("jobCardList", [])
            
            if not job_list:
                print(f"第 {page} 页没有数据")
                break
            
            print(f"第 {page} 页共 {len(job_list)} 个职位")
            
            # 遍历每个职位
            for idx, job_item in enumerate(job_list, 1):
                # 检查是否已达到目标数量
                if len(all_data) >= max_count:
                    print(f"\n已达到目标数量 {max_count} 条，停止爬取")
                    break
                
                job = job_item.get("job", {})
                job_url = job.get("link", "")
                job_title = job.get("title", "")
                
                if not job_url:
                    print(f"  [{idx}] {job_title} - 无详情链接，跳过")
                    continue
                
                print(f"  [{idx}] 正在爬取: {job_title}")
                
                # 获取职位详情
                detail_info = self.get_job_detail(job_url)
                
                # 解析并保存数据
                job_data = self.parse_job_data(job_item, detail_info)
                all_data.append(job_data)
                
                # 延迟，避免请求过快
                time.sleep(1)
            
            # 如果已达到目标数量，退出循环
            if len(all_data) >= max_count:
                break
            
            # 页面间延迟
            page += 1
            time.sleep(2)
        
        # 保存所有数据
        if all_data:
            self.save_to_csv(all_data)
        
        return all_data


if __name__ == "__main__":
    spider = LiepinSpider()
    
    # 爬取武汉地区的人工智能职位，爬取100条数据
    data = spider.run(keyword="人工智能", city="410", max_count=100)
    
    print(f"\n爬取完成！共获取 {len(data)} 条数据")
