---
title: Skywalking使用graphql查询
date: 2022-12-15 23:12:12
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - Skywalking使用graphql查询
---
#### 查询单个服务的数据信息

```java
{
	"query":
	"query queryData($serviceId: ID!,$duration: Duration!) {
	  serviceApdexScore: getLinearIntValues(metric: {
	    name: \"service_apdex\"
	    id: $serviceId
	  }, duration: $duration) {
	    values {value}
	  }
	  serviceResponseTime: getLinearIntValues(metric: {
	    name: \"service_resp_time\"
	    id: $serviceId
	  }, duration: $duration) {
	    values {value}
	  }
	  serviceThroughput: getLinearIntValues(metric: {
	    name: \"service_cpm\"
	    id: $serviceId
	  }, duration: $duration) {
	    values {
	      value
	    }
	  }
	  serviceSLA: getLinearIntValues(metric: {
	    name: \"service_sla\"
	    id: $serviceId
	  }, duration: $duration) {
	    values {
	      value
	    }
	  }
	  globalPercentile: getMultipleLinearIntValues(metric: {
	    name: \"all_percentile\"
	  }, numOfLinear: 5, duration: $duration) { values { value } }
	  servicePercentile: getMultipleLinearIntValues(metric: {
	    name: \"service_percentile\"
	    id: $serviceId
	  }, numOfLinear: 5, duration: $duration) { values { value } }
	  serviceSlowEndpoint: getEndpointTopN(
	    serviceId: $serviceId
	    duration: $duration
	    name: \"endpoint_avg\",
	    topN: 10,
	    order: DES
	  ) {
	    key: id
	    label: name
	    value
	  }
	  serviceInstanceThroughput: getServiceInstanceTopN(
	    serviceId: $serviceId
	    duration: $duration
	    name: \"service_instance_cpm\",
	    topN: 10,
	    order: DES
	  ) {
	    key: id
	    label: name
	    value
	  }}",
	
	"variables":{
		"atabaseId":"",
		"duration":{"start": "2020-05-18", "end": "2020-05-21", "step": "DAY"},
		"endpointId":"4",
		"endpointName":"/api/items",
		"instanceId":"5",
		"serviceId":"4"
	}
}
{"data":{"serviceApdexScore":{"values":[{"value":0},{"value":0},{"value":0},{"value":10000}]},"serviceResponseTime":{"values":[{"value":0},{"value":0},{"value":0},{"value":380}]},"serviceThroughput":{"values":[{"value":0},{"value":0},{"value":0},{"value":0}]},"serviceSLA":{"values":[{"value":0},{"value":0},{"value":0},{"value":10000}]},"globalPercentile":[{"values":[{"value":0},{"value":0},{"value":0},{"value":370}]},{"values":[{"value":0},{"value":0},{"value":0},{"value":410}]},{"values":[{"value":0},{"value":0},{"value":0},{"value":410}]},{"values":[{"value":0},{"value":0},{"value":0},{"value":1560}]},{"values":[{"value":0},{"value":0},{"value":0},{"value":1560}]}],"servicePercentile":[{"values":[{"value":0},{"value":0},{"value":0},{"value":370}]},{"values":[{"value":0},{"value":0},{"value":0},{"value":380}]},{"values":[{"value":0},{"value":0},{"value":0},{"value":380}]},{"values":[{"value":0},{"value":0},{"value":0},{"value":380}]},{"values":[{"value":0},{"value":0},{"value":0},{"value":380}]}],"serviceSlowEndpoint":[{"key":"4","label":"/api/items","value":380}],"serviceInstanceThroughput":[{"key":"5","label":"provider-pid:4920@KFW7BT1P01V035","value":0}]}}
```

#### 2. 查询一段时间内的服务id和名称

```java
{
  "query": "query queryServices($duration: Duration!) {services: getAllServices(duration: $duration) {id, name}}",
  "variables": {
    "duration": {
      "start": "2020-05-21",
      "end": "2020-05-22",
      "step": "DAY"
    }
  }
}
{
    "data": {
        "services": [
            {
                "id": "3",
                "name": "consumer"
            },
            {
                "id": "7",
                "name": "SpringBootWithSkywalking-HelloTomcat"
            },
            {
                "id": "2",
                "name": "hello-world-demo"
            },
            {
                "id": "4",
                "name": "provider"
            }
        ]
    }
}
```

获得服务的id和name，可以用来查询响应时间、可用性等指标

#### 3. 根据服务id数组查询响应时间、服务apdex分数、slas数、吞吐量

```java
{
	"query":
		"query queryData($serviceIds: [ID!]!,$duration: Duration!) {
			serviceResponseTime: getValues(metric: {
		    	name: \"service_resp_time\"
				 ids: $serviceIds
			}, duration: $duration) {
				  values {id, value}
				 }
			serviceApdexScore: getValues(metric: {
				 name: \"service_apdex\"
				 ids: $serviceIds
			}, duration: $duration) {
				    values { id,value}
				 }
		    serviceSLA: getValues(metric: {
			    name: \"service_sla\"
			    ids: $serviceIds
			}, duration: $duration) {
			    values {id, value}
				}
			serviceThroughput: getValues(metric: {
			    name: \"service_cpm\"
			    ids: $serviceIds
			}, duration: $duration) {
			    values {id, value}
				}
			
		}",
	
	"variables":{
			"duration":{"start": "2020-05-21", "end": "2020-05-22", "step": "DAY"},
			"serviceIds":["2","3","4","7"]
	}
}
{
    "data": {
        "serviceResponseTime": {
            "values": [
                {
                    "id": "2",
                    "value": 191
                },
                {
                    "id": "3",
                    "value": 989
                },
                {
                    "id": "4",
                    "value": 380
                },
                {
                    "id": "7",
                    "value": 144
                }
            ]
        },
        "serviceApdexScore": {
            "values": [
                {
                    "id": "2",
                    "value": 10000
                },
                {
                    "id": "3",
                    "value": 7500
                },
                {
                    "id": "4",
                    "value": 10000
                },
                {
                    "id": "7",
                    "value": 10000
                }
            ]
        },
        "serviceSLA": {
            "values": [
                {
                    "id": "2",
                    "value": 10000
                },
                {
                    "id": "3",
                    "value": 10000
                },
                {
                    "id": "4",
                    "value": 10000
                },
                {
                    "id": "7",
                    "value": 10000
                }
            ]
        },
        "serviceThroughput": {
            "values": [
                {
                    "id": "2",
                    "value": 0
                },
                {
                    "id": "3",
                    "value": 0
                },
                {
                    "id": "4",
                    "value": 0
                },
                {
                    "id": "7",
                    "value": 0
                }
            ]
        }
    }
}
```