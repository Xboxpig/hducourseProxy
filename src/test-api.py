from hdu_api import HduCourseSession
import json

# 传入你提供的最新参数
RAW_TOKEN = "eyJhbGciOiJSUzI1NiJ9.eyJhdXRoVXNlckRldGFpbHMiOiJ7XCJ1c2VyXCI6IHtcImNvZGVcIjogXCJkYzgxMWY4Yy05YzgzLTRjYzktOTY4OC1iNzM0ZjVjNjExY2FcIn19Iiwic3ViIjoiMjMwNjA5MDkiLCJkZWZhdWx0R3JhbnRTY29wZSI6Imp5LWFwcGxpY2F0aW9uLXZvZC1oZSxqeS1hcHBsaWNhdGlvbi12b2QtaGUsY2xvdWQtcmJhYyIsImFtciI6Im1mYSIsImlzcyI6Imh0dHA6Ly9kZXYuY3RzcC5rZWRhY29tLmNvbS9jbG91ZC1yYmFjIiwiYXV0aFRpbWUiOjE3NjcwNTk4OTU1MDIsImFjY2Vzc1Rva2VuIjoibWpDQStkNUJJbFZqejl3M0w4MkUwaERzNGtyQTc3QU1GZkQ3SERPL1FjdzZwZzFYdzBtUTBzRkNWY3kvRFFqdVZ6RXJwTndUUHoxVnRxcmNlaEFOQXd5ZGFOVEpTSnF4aHVjbENIcUlOUWM9Iiwibm9uY2UiOiI4YTI2MzMwNy0yZTU2LTQ3NTAtODQzYS0xODJhZGVlM2E4MmUiLCJhdWQiOiJqeS1hcHBsaWNhdGlvbi12b2QtaGUiLCJhY3IiOiJ1cm46bWFjZTppbmNvbW1vbjppYXA6c2lsdmVyIiwiYXpwIjoiIiwidGVuYW50SWQiOiJSQkFDIiwiZXhwIjoxNzY3MDU5ODk1LCJpYXQiOjE3NjY5NzM0OTV9.AnpQuaja6fb6rOCtHIKbISgP5ZrD_uo_MqxSAMIp5KvAWLufRYLL0r0Rt5KJCPToMJiNGVF9x1dos_XHKPc7RQ"
RAW_COOKIE = "route=1766973491.17.4051.620062; jy-application-vod-he=OGEyNjMzMDctMmU1Ni00NzUwLTg0M2EtMTgyYWRlZTNhODJl"

def main():
    # 1. 初始化类实例
    api = HduCourseSession(RAW_TOKEN, RAW_COOKIE)
    
    print("[*] 正在同步今日课程列表...")
    
    # 2. 调用获取列表方法
    courses = api.fetch_live_courses()
    
    if not courses:
        print("[-] 未能获取课程，请确认 Token 是否已失效。")
        return

    print(f"[+] 成功同步 {len(courses)} 门课程：\n")
    print(f"{'序号':<4} | {'ID':<10} | {'老师':<8} | {'课程名称'}")
    print("-" * 60)
    
    for idx, c in enumerate(courses, 1):
        print(f"{idx:<4} | {c['id']:<10} | {c['teacher']:<8} | {c['name']}")

    # 3. 自动测试获取第一个课程的流地址
    first_id = courses[0]['id']
    print(f"\n[*] 正在自动解析 ID 为 {first_id} 的原始视频流...")
    
    stream_url = api.get_stream_url(first_id)
    
    if stream_url:
        print("\n[🔥 解析成功] 最终推流地址：")
        print(stream_url)
    else:
        print("\n[-] 流地址解析失败。")

if __name__ == "__main__":
    main()