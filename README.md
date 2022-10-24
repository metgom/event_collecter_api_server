# igaworks_api_server

서버는 EC2 인스턴스 내에서 Nginx와 API Server를 각각 Docker로 실행하고 있습니다.  
외부 연결은 Nginx가 담당하고 리버스 프록시로 Nginx와 API Server를 연결하도록 구성하였습니다.  
API Server는 FastAPI로 작성하였습니다.  
> Client <=> nginx <=> API Server  

엔드포인트는 다음과 같습니다.
- Event Collect API : 이벤트를 수집합니다.  
  - http://ec2-52-79-98-181.ap-northeast-2.compute.amazonaws.com:8080/api/collect 또는  
  - http://ec2-52-79-98-181.ap-northeast-2.compute.amazonaws.com:8080/api/event  

Method : POST
> Reuqest Body :  
```
{  
  "event_id": "string",  
  "event": "string",  
  "event_datetime": "2022-10-24T07:41:45.087Z",  
  "user_id": "string",  
  "parameters": {  
    "order_id": "string,  
    "currency": "string",  
    "price": 0  
  }  
}  
```

> Response :  Json
```
{  
	"is_success": "true" or "false"  
}  
```


- Event Search API : user_id와 부분 일치하는 이벤트 데이터를 검색합니다.  
  - http://ec2-52-79-98-181.ap-northeast-2.compute.amazonaws.com:8080/api/search 또는  
  - http://ec2-52-79-98-181.ap-northeast-2.compute.amazonaws.com:8080/api/event/{user_id}

http://ec2-52-79-98-181.ap-northeast-2.compute.amazonaws.com:8080/api/search  
Method : POST
> Reuqest Body : 
```
{
  "user_id" : "string"
}
```
http://ec2-52-79-98-181.ap-northeast-2.compute.amazonaws.com:8080/api/event/  
http://ec2-52-79-98-181.ap-northeast-2.compute.amazonaws.com:8080/api/event/{user_id}  
Method : GET
> Reuqest Parameters : 
```
user_id = "string"
```
> Response :  Json
```
{
  "event_id": "string",
  "event": "string",
  "event_datetime": "%Y-%m-%dT%H:%M:%S.%fZ",
  "parameters": null or 
  {
    "order_id": "string",
    "currency": "string",
    "price": "float"
  }
}
```
