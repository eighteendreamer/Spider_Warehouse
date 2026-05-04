import requests
import json
import re
import csv
import os
import time


headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/json",
    "device": "pc",
    "origin": "https://www.iguopin.com",
    "priority": "u=1, i",
    "referer": "https://www.iguopin.com/",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "subsite": "iguopin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0"
}
url = "https://gp-api.iguopin.com/api/jobs/v1/recom-job"


def parse_contents(contents):
    """解析contents字段，拆分为职责和能力要求"""
    if not contents:
        return "", ""

    req_pattern = r'(任职要求|职位要求|任职资格|岗位要求|岗位条件|招聘要求)[：:]*'
    duty_pattern = r'(工作职责|岗位职责|职位描述|工作内容)[：:]*'

    req_match = re.search(req_pattern, contents)
    if req_match:
        duty_part = contents[:req_match.start()].strip()
        req_part = contents[req_match.end():].strip()
    else:
        duty_match = re.search(duty_pattern, contents)
        if duty_match:
            duty_part = contents[duty_match.end():].strip()
        else:
            duty_part = contents
        req_part = ""

    duty_clean = re.sub(r'^(' + '|'.join(['工作职责', '岗位职责', '职位描述', '工作内容']) + r')[：:]*\s*', '', duty_part).strip()
    req_clean = re.sub(r'^(' + '|'.join(['任职要求', '职位要求', '任职资格', '岗位要求', '岗位条件', '招聘要求']) + r')[：:]*\s*', '', req_part).strip()

    return duty_clean, req_clean


def format_salary(min_wage, max_wage, wage_unit_cn="元/月"):
    """格式化薪资"""
    if min_wage == 0 and max_wage == 0:
        return "面议"
    if min_wage and max_wage:
        return f"{min_wage}-{max_wage}{wage_unit_cn}"
    elif min_wage:
        return f"{min_wage}{wage_unit_cn}起"
    elif max_wage:
        return f"最高{max_wage}{wage_unit_cn}"
    return "面议"


# 分页爬取100条数据
total_target = 100
page_size = 20
all_records = []

for page in range(1, (total_target // page_size) + 1):
    data = {
        "search": {
            "page": page,
            "page_size": page_size,
            "keyword": "人工智能"
        },
        "recom": {
            "update_time": True,
            "company_nature": True,
            "hot_job": True
        }
    }
    data_str = json.dumps(data, separators=(',', ':'))

    print(f"正在爬取第 {page} 页...")
    response = requests.post(url, headers=headers, data=data_str)
    result = response.json()

    job_list = result.get("data", {}).get("list", [])
    if not job_list:
        print(f"第 {page} 页无数据，停止爬取")
        break

    for job in job_list:
        company_name = job.get("company_name", "")
        job_name = job.get("job_name", "")
        scale_cn = job.get("company_info", {}).get("scale_cn", "")
        contents = job.get("contents", "")
        min_wage = job.get("min_wage", 0)
        max_wage = job.get("max_wage", 0)
        wage_unit_cn = job.get("wage_unit_cn", "元/月")

        duty, requirement = parse_contents(contents)
        salary = format_salary(min_wage, max_wage, wage_unit_cn)

        all_records.append({
            "求职网站": "国聘",
            "公司名称": company_name,
            "岗位名": job_name,
            "需求数量": scale_cn,
            "职责": duty,
            "能力要求": requirement,
            "薪资待遇": salary
        })

    total = result.get("data", {}).get("total", 0)
    print(f"  本页获取 {len(job_list)} 条，累计 {len(all_records)} 条，总数据量 {total}")

    if len(all_records) >= total_target:
        break

    time.sleep(1)

# 截取前100条
all_records = all_records[:total_target]

# 追加写入CSV
csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "招聘.csv")
file_exists = os.path.exists(csv_path)

fieldnames = ["求职网站", "公司名称", "岗位名", "需求数量", "职责", "能力要求", "薪资待遇"]
with open(csv_path, "a", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    if not file_exists:
        writer.writeheader()
    writer.writerows(all_records)

print(f"\n共爬取 {len(all_records)} 条数据，已追加保存到 {csv_path}")
