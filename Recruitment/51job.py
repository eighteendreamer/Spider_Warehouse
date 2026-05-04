
import requests
import json
import re
import csv
import os
from typing import Dict, List, Optional


def parse_job_description(job_desc: str) -> Dict[str, str]:
    """
    解析职位描述，提取职责和要求
    查找常见模式如'岗位职责'、'任职资格'、'工作内容'、'岗位要求'
    """
    if not job_desc:
        return {"responsibilities": "", "requirements": ""}
    
    # 规范化换行符和空白字符
    job_desc = re.sub(r'\s+', ' ', job_desc.strip())
    
    # 按常见章节分隔符拆分
    sections = {}
    
    # 查找章节标题
    # 中文章节标题的正则模式
    section_patterns = [
        r'(?:岗位职责|工作内容|岗位内容|工作职责|主要职责|职责要求)[:：\s]*([^\n]+?)(?=(?:岗位职责|任职资格|岗位要求|工作要求|职位要求|岗位条件|招聘要求|任职条件|能力要求|技能要求|任职条件|岗位要求|$))',
        r'(?:任职资格|岗位要求|工作要求|职位要求|岗位条件|招聘要求|任职条件|能力要求|技能要求|任职条件|岗位要求)[:：\s]*([^\n]+?)(?=(?:岗位职责|任职资格|岗位要求|工作要求|职位要求|岗位条件|招聘要求|任职条件|能力要求|技能要求|任职条件|岗位要求|$))'
    ]
    
    # 首先尝试查找结构化章节
    responsibilities = ""
    requirements = ""
    
    # 查找"岗位职责"章节
    resp_match = re.search(r'(?:岗位职责|工作内容|岗位内容|工作职责|主要职责|职责要求|岗位职责描述|工作描述)[:：\s]*(.*?)(?=(?:任职资格|任职要求|岗位要求|工作要求|职位要求|岗位条件|招聘要求|任职条件|能力要求|技能要求|任职条件|岗位要求|$))', job_desc, re.DOTALL | re.IGNORECASE)
    if resp_match:
        responsibilities = resp_match.group(1).strip()
    
    # 查找"任职要求"或"任职资格"章节
    req_match = re.search(r'(?:任职要求|任职资格|岗位要求|工作要求|职位要求|岗位条件|招聘要求|任职条件|能力要求|技能要求|任职条件|岗位要求)[:：\s]*(.*?)(?=(?:岗位职责|工作内容|岗位内容|工作职责|主要职责|职责要求|岗位职责描述|工作描述|$))', job_desc, re.DOTALL | re.IGNORECASE)
    if req_match:
        requirements = req_match.group(1).strip()
    
    # 如果没有找到结构化章节，使用后备逻辑
    if not responsibilities and not requirements:
        # 尝试按常见分隔符拆分
        if '岗位职责' in job_desc or '工作内容' in job_desc:
            parts = re.split(r'(?:岗位职责|工作内容|岗位内容|工作职责|主要职责|职责要求)', job_desc)
            if len(parts) > 1:
                responsibilities = parts[1].split('任职资格')[0].strip() if '任职资格' in parts[1] else parts[1].strip()
                if '任职资格' in job_desc:
                    req_parts = re.split(r'(?:任职资格|岗位要求|工作要求|职位要求)', job_desc)
                    if len(req_parts) > 1:
                        requirements = req_parts[1].strip()
        elif '任职资格' in job_desc or '岗位要求' in job_desc:
            parts = re.split(r'(?:任职资格|岗位要求|工作要求|职位要求)', job_desc)
            if len(parts) > 1:
                requirements = parts[1].strip()
        else:
            # 默认：将所有内容放入职责
            responsibilities = job_desc.strip()
    
    # 清理提取的文本
    responsibilities = re.sub(r'\s+', ' ', responsibilities).strip()
    requirements = re.sub(r'\s+', ' ', requirements).strip()
    
    return {
        "responsibilities": responsibilities,
        "requirements": requirements
    }


def extract_jobs_from_api() -> List[Dict]:
    """
    从51Job API提取职位数据
    返回包含所需字段的字典列表
    """

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "account-id;": "",
        "cache-control": "no-cache",
        "from-domain": "51job_web",
        "partner": "www_google_com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "property": "%7B%22partner%22%3A%22www_google_com%22%2C%22webId%22%3A2%2C%22fromdomain%22%3A%2251job_web%22%2C%22frompageUrl%22%3A%22https%3A%2F%2Fwe.51job.com%2F%22%2C%22pageUrl%22%3A%22https%3A%2F%2Fwe.51job.com%2Fpc%2Fsearch%3FjobArea%3D060000%26keyword%3D%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%26searchType%3D2%26keywordType%3D%22%2C%22identityType%22%3A%22%22%2C%22userType%22%3A%22%22%2C%22isLogin%22%3A%22%E5%90%A6%22%2C%22accountid%22%3A%22%22%2C%22keywordType%22%3A%22%22%7D",
        "referer": "https://we.51job.com/pc/search?jobArea=060000&keyword=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&searchType=2&keywordType=",
        "sec-ch-ua": "\"Google Chrome\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sign": "6e73e9f82570304d8419838ee07bca3fb12e5e937b305f0d0f58f5a87cf74e78",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
        "user-token;": "",
        "uuid": "3b68bcdf52d2dc7522ef7ac0c50eb431"
    }
    cookies = {
        "_c_i_p": "060000",
        "sajssdk_2015_cross_new_user": "1",
        "Hm_lvt_1370a11171bd6f2d9b1fe98951541941": "1777868220",
        "HMACCOUNT": "6DC40D2860C660F6",
        "guid": "3b68bcdf52d2dc7522ef7ac0c50eb431",
        "partner": "www_google_com",
        "seo_refer_info_2023": "%7B%22referUrl%22%3A%22https%3A%5C%2F%5C%2Fwww.google.com%5C%2F%22%2C%22referHost%22%3A%22www.google.com%22%2C%22landUrl%22%3A%22https%3A%5C%2F%5C%2Fwww.51job.com%5C%2F%22%2C%22landHost%22%3A%22www.51job.com%22%2C%22partner%22%3A%22www_google_com%22%7D",
        "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%223b68bcdf52d2dc7522ef7ac0c50eb431%22%2C%22first_id%22%3A%2219df13423d49fc-06b2646ef7ec55c-26061e51-1327104-19df13423d5d80%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTlkZjEzNDIzZDQ5ZmMtMDZiMjY0NmVmN2VjNTVjLTI2MDYxZTUxLTEzMjcxMDQtMTlkZjEzNDIzZDVkODAiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIzYjY4YmNkZjUyZDJkYzc1MjJlZjdhYzBjNTBlYjQzMSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%223b68bcdf52d2dc7522ef7ac0c50eb431%22%7D%2C%22%24device_id%22%3A%2219df13b05212be-09aa2ccf0c267d-26061e51-1327104-19df13b05221958%22%7D",
        "Hm_lpvt_1370a11171bd6f2d9b1fe98951541941": "1777868703",
        "acw_tc": "ac11000117778702204844042e00a5d0d2da8bba0c05015765e73a8811e485",
        "acw_sc__v2": "69f825962e363105ffcc27b1541a1490300c74f3",
        "JSESSIONID": "0C23479DA971DB710182837585639400",
        "ssxmod_itna": "1-eqfxyDRDBDuD9DRO7Dh=GDRDI=7D8lDeToe0dGMD3de7tQGcD8xx0PKSxPjRoqqPqDGxxqq1C0dYNDlaAeDZDGFQDqx0Eb2lAigD54oW7iTeKm0w0wp3CBEO85dOG010p9d0i285ezLFxXUMUbYAeDU4GnD06gBxoD4R3Dt4DIDAYDDxDWj4DLDYoDY4WYxGpQVCnbuCRWD0YDzqDgD7jWReDEDG3D03TK4RhGRjb3DDtDAd9wkPDADA3tq4Dl4SShY77DboTrTC9Wf=OKe1GxReDM7xGXYG1_NUZyq4ardVl6H8R7wPGuDDkB4WdfFnGTf_Wi8kp7tRxxpiodAi=hxgD4zYYN0qpDxt0xY7xqiw3xwuoYK0qQGxlY_6Wotw5q0ppC_lMs4QTenGpixl7N9oAefYzQY8qYiAwl05ViYnoQxOIeD4iA=oGDiW_o6wYitG2qiDppEoPSppYE27I3oY4D",
        "ssxmod_itna2": "1-eqfxyDRDBDuD9DRO7Dh=GDRDI=7D8lDeToe0dGMD3de7tQGcD8xx0PKSxPjRoqqPqDGxxqq1C0d7oDiaRYxp33D7Pexv/QYD/iQZ345Knzp0WKqKN10aKkw2i6quU5nZlC62ROFhOnuU4mfGYNel734GwxKRMt4tj64Muw/iD_bWfeQyWoeB2vseRi4FkDtN=YxD"
    }
    url = "https://we.51job.com/api/job/search-pc"
    params = {
        "api_key": "51job",
        "timestamp": "1777868475",
        "keyword": "人工智能",
        "searchType": "2",
        "function": "",
        "industry": "",
        "jobArea": "060000",
        "jobArea2": "",
        "landmark": "",
        "metro": "",
        "salary": "",
        "workYear": "",
        "degree": "",
        "companyType": "",
        "companySize": "",
        "jobType": "",
        "issueDate": "",
        "sortType": "0",
        "pageNum": "1",
        "requestId": "",
        "keywordType": "",
        "pageSize": "100",
        "source": "1",
        "accountId": "",
        "pageCode": "sou|sou|soulb",
        "scene": "7"
    }
    
    try:
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        response.raise_for_status()
        
        # 解析JSON响应
        data = response.json()
        
        # 提取职位列表
        if "resultbody" in data and "job" in data["resultbody"] and "items" in data["resultbody"]["job"]:
            job_items = data["resultbody"]["job"]["items"]
        else:
            print("Error: Unexpected JSON structure")
            return []
        
        # 最多处理100条职位
        results = []
        for i, job in enumerate(job_items[:100]):
            # 提取所需字段
            full_company_name = job.get("fullCompanyName", "")
            job_name = job.get("jobName", "")
            company_size_string = job.get("companySizeString", "")
            job_describe = job.get("jobDescribe", "")
            provide_salary_string = job.get("provideSalaryString", "")
            
            # 解析职位描述
            parsed_desc = parse_job_description(job_describe)
            
            # 构建结果字典
            result = {
                "求职网站": "51Job",
                "公司名称": full_company_name,
                "岗位名": job_name,
                "需求数量": company_size_string,
                "职责": parsed_desc["responsibilities"],
                "能力要求": parsed_desc["requirements"],
                "薪资待遇": provide_salary_string
            }
            
            results.append(result)
            
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


def save_to_csv(jobs: List[Dict]) -> None:
    """
    以追加模式将职位数据保存到CSV文件
    """
    csv_file_path = "data/招聘.csv"
    
    try:
        # 检查文件是否存在且已有内容（表头已存在）
        file_has_content = os.path.isfile(csv_file_path) and os.path.getsize(csv_file_path) > 0
        
        # 以追加模式打开文件
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["求职网站", "公司名称", "岗位名", "需求数量", "职责", "能力要求", "薪资待遇"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # 仅当文件新建或为空时写入表头
            if not file_has_content:
                writer.writeheader()
            
            # 写入职位数据
            for job in jobs:
                # 转义引号并处理特殊字符
                escaped_job = {}
                for key, value in job.items():
                    if isinstance(value, str):
                        # 将双引号替换为两个双引号以适配CSV格式
                        escaped_value = value.replace('"', '""')
                        escaped_job[key] = escaped_value
                    else:
                        escaped_job[key] = value
                
                writer.writerow(escaped_job)
        
        print(f"\n成功将 {len(jobs)} 条职位信息追加保存到 {csv_file_path}")
        
    except Exception as e:
        print(f"保存CSV文件时出错: {e}")

def main():
    """
    主函数：运行爬虫并展示结果
    """
    print("正在从51Job获取招聘信息...")
    
    jobs = extract_jobs_from_api()
    
    if not jobs:
        print("未获取到任何职位信息")
        return
    
    print(f"\n成功获取 {len(jobs)} 条职位信息：\n")
    
    for i, job in enumerate(jobs, 1):
        print(f"--- 第 {i} 条职位信息 ---")
        print(f"求职网站: {job['求职网站']}")
        print(f"公司名称: {job['公司名称']}")
        print(f"岗位名: {job['岗位名']}")
        print(f"需求数量: {job['需求数量']}")
        print(f"职责: {job['职责']}")
        print(f"能力要求: {job['能力要求']}")
        print(f"薪资待遇: {job['薪资待遇']}")
        print()
    
    # 以追加模式将结果保存到CSV文件
    save_to_csv(jobs)

if __name__ == "__main__":
    main()