import http.client
import json

# 1. تصحيح: استخدام HTTPConnection بدلاً من HTTPSConnection
conn = http.client.HTTPConnection("127.0.0.1", 8000) 

# **ملاحظة:** تأكد من أن الـ Access Token (رمز الوصول) صحيح وغير منتهٍ صلاحيته
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0NjE3MzA5LCJpYXQiOjE3NjQ2MTcwMDksImp0aSI6IjJlNjFiYmJjMDk1YTRkNWE5MjY5NzlmMWJkMTRiNjJkIiwidXNlcl9pZCI6IjIifQ.CYggfVN3XzjfA27DvWMcWFnox6imER8z4HpIRUv8HwI"

headersList = {
"Accept": "*/*",
"User-Agent": "Thunder Client (https://www.thunderclient.com)",
"Content-Type": "application/json",
"Authorization": f"Bearer {ACCESS_TOKEN}" # استخدام الرمز الجديد
}

# 2. تصحيح: إلغاء الـ payload لأنه طلب GET
payload = None 

conn.request("GET", "/api/core/profile/", payload, headersList)
response = conn.getresponse()
result = response.read()

print(result.decode("utf-8"))