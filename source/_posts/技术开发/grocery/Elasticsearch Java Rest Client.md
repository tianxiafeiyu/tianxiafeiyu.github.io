基于 Elasticsearch 6.x

## 概述

Rest client 分成两部分：

- Java Low Level REST Client
  官方低级别 es 客户端，使用 http 协议与 Elastiicsearch 集群通信，与所有 es 版本兼容。
- Java High level REST Client
  官方高级别 es 客户端，基于低级别的客户端，它会暴露 API 特定的方法。

使用方法：

```java
<dependency>
    <groupId>org.elasticsearch.client</groupId>
    <artifactId>elasticsearch-rest-high-level-client</artifactId>
    <version>6.3.2</version>
</dependency>
```

初始化：

```java
RestHighLevelClient client = new RestHighLevelClient(
        RestClient.builder(
                new HttpHost("localhost", 9200, "http"),
                new HttpHost("localhost", 9201, "http")));
```

## 文档(Document) API

单文档 API

- index API
- Get API
- Delete API
- Update API

多文档 API

- Bulk API
- Multi-Get API

### Index API

#### IndexRequest

四种方式构建 IndexRequest：

1. json

```java
IndexRequest indexRequest = new IndexRequest(
        "posts",  // 索引 Index
        "doc",  // Type 
        "1");  // 文档 Document Id 
String jsonString = "{" +
        "\"user\":\"kimchy\"," +
        "\"postDate\":\"2013-01-30\"," +
        "\"message\":\"trying out Elasticsearch\"" +
        "}";
indexRequest.source(jsonString, XContentType.JSON); // 文档源格式为 json string
```

1. Map

```java
Map<String, Object> jsonMap = new HashMap<>();
jsonMap.put("user", "kimchy");
jsonMap.put("postDate", new Date());
jsonMap.put("message", "trying out Elasticsearch");
IndexRequest indexRequest = new IndexRequest("posts", "doc", "1")
        .source(jsonMap);  // 会自动将 Map 转换为 JSON 格式
```

1. XContentBuilder : Document Source 提供的帮助类，专门用来产生 json 格式的数据

```java
XContentBuilder builder = XContentFactory.jsonBuilder();
builder.startObject();
{
    builder.field("user", "kimchy");
    builder.timeField("postDate", new Date());
    builder.field("message", "trying out Elasticsearch");
}
builder.endObject();
IndexRequest indexRequest = new IndexRequest("posts", "doc", "1")
        .source(builder); 
```

1. Object 键值对

```java
IndexRequest indexRequest = new IndexRequest("posts", "doc", "1")
        .source("user", "kimchy",
                "postDate", new Date(),
                "message", "trying out Elasticsearch"); 
```

#### 同步索引

```java
IndexResponse indexResponse = client.index(indexRequest);
```

#### 异步索引

异步执行函数需要添加 listener 作为回调函数, 而对于 index 而言，这个 listener 的类型就是 ActionListener

```java
ActionListener<IndexResponse> listener = new ActionListener<IndexResponse>() {
    @Override
    public void onResponse(IndexResponse indexResponse) { //执行成功，调用 onResponse 函数
        
    }

    @Override
    public void onFailure(Exception e) { //执行失败，调用 onFailure 函数
        
    }
};

IndexResponse indexResponse = client.indexAsync(indexRequest, listener); 
```

#### IndexResponse

不管是同步还是异步，如果调用成功，都会返回 IndexRespose 对象。

```java
tring index = indexResponse.getIndex();
String type = indexResponse.getType();
String id = indexResponse.getId();
long version = indexResponse.getVersion();
if (indexResponse.getResult() == DocWriteResponse.Result.CREATED) {
   // 文档第一次创建 
} else if (indexResponse.getResult() == DocWriteResponse.Result.UPDATED) {
   // 文档之前已存在，当前是重写
}
ReplicationResponse.ShardInfo shardInfo = indexResponse.getShardInfo();
if (shardInfo.getTotal() != shardInfo.getSuccessful()) {
    // 成功的分片数量少于总分片数量 
}
if (shardInfo.getFailed() > 0) {
    for (ReplicationResponse.ShardInfo.Failure failure : shardInfo.getFailures()) {
        String reason = failure.reason();  // 处理潜在的失败信息
    }
}
```

### GET API

#### GetRequest

每个 GET 请求都必须需传入下面 3 个参数：

- Index
- Type
- Document id

```java
GetRequest getRequest = new GetRequest(
        "posts", 
        "doc",  
        "1");   
```

可选参数：

1. 不获取源数据，默认是获取的

```java
getRequest.fetchSourceContext(FetchSourceContext.DO_NOT_FETCH_SOURCE); 
```

1. 配置返回数据中包含指定字段

```java
String[] includes = new String[]{"message", "*Date"};
String[] excludes = Strings.EMPTY_ARRAY;
FetchSourceContext fetchSourceContext =
        new FetchSourceContext(true, includes, excludes);
getRequest.fetchSourceContext(fetchSourceContext); 
```

1. 配置返回数据中排除指定字段

```java
String[] includes = Strings.EMPTY_ARRAY;
String[] excludes = new String[]{"message"};
FetchSourceContext fetchSourceContext =
        new FetchSourceContext(true, includes, excludes);
getRequest.fetchSourceContext(fetchSourceContext); 
```

1. 实时 默认为 true

```
getRequest.realtime(false);
```

1. 版本

```
getRequest.version(2); 
```

1. 版本类型

```
getRequest.versionType(VersionType.EXTERNAL);
```

#### 执行

同步执行：

```
GetResponse getResponse = client.get(getRequest);
```

异步执行：

```
ActionListener<IndexResponse> listener = new ActionListener<IndexResponse>() {
    @Override
    public void onResponse(IndexResponse indexResponse) { //执行成功，调用 onResponse 函数
        
    }

    @Override
    public void onFailure(Exception e) { //执行失败，调用 onFailure 函数
        
    }
};

GetResponse getResponse = client.indexAsync(indexRequest, listener); 
```

#### GetResponse

返回的 GetResponse 对象包含要请求的文档数据（包含元数据和字段）

```java
String index = getResponse.getIndex();
String type = getResponse.getType();
String id = getResponse.getId();
if (getResponse.isExists()) {
    long version = getResponse.getVersion();
    String sourceAsString = getResponse.getSourceAsString(); // string 形式   
    Map<String, Object> sourceAsMap = getResponse.getSourceAsMap(); // map 
    byte[] sourceAsBytes = getResponse.getSourceAsBytes(); // 字节形式 
} else {
   // 没有发现请求的文档 
}
```

### Exists API

如果文档存在 Exists API 返回 true, 否则返回 fasle。

#### GetRequest

用法和 Get API 差不多，两个对象的可选参数是相同的。由于 exists() 方法只返回 true 或者 false， 应该将获取 _source 以及任何存储字段的值关闭，尽量使请求轻量级。

```java
GetRequest getRequest = new GetRequest(
    "posts",  // Index
    "doc",    // Type
    "1");     // Document id
getRequest.fetchSourceContext(new FetchSourceContext(false));  // 禁用 _source 字段
getRequest.storedFields("_none_"); // 禁止存储任何字段   
```

#### 执行

同步执行：

```java
boolean exists = client.exists(getRequest);
```

异步执行：

```java
ActionListener<Boolean> listener = new ActionListener<Boolean>() {
    @Override
    public void onResponse(Boolean exists) {
        
    }

    @Override
    public void onFailure(Exception e) {
        
    }
};

boolean exists = client.existsAsync(getRequest, listener); 
```

### Delete API

#### DeleteRequest

DeleteRequest 必须传入下面参数：

- Index
- Type
- Document id

```java
DeleteRequest deleteRequest = new DeleteRequest(
        "posts",   // index 
        "doc",     // doc
        "1");      // document id
```

可选参数：

1. 超时时间

```java
deleteRequest.timeout(TimeValue.timeValueMinutes(2)); 
deleteRequest.timeout("2m"); 
```

1. 刷新策略

```java
deleteRequest.setRefreshPolicy(WriteRequest.RefreshPolicy.WAIT_UNTIL); 
deleteRequest.setRefreshPolicy("wait_for");    
```

1. 版本

```java
deleteRequest.version(2); 
```

1. 版本类型

```java
deleteRequest.versionType(VersionType.EXTERNAL); 
```

#### 执行

同步执行：

```java
DeleteResponse deleteResponse = client.delete(deleteRequest);
```

异步执行

```java
ActionListener<DeleteResponse> listener = new ActionListener<DeleteResponse>() {
    @Override
    public void onResponse(DeleteResponse deleteResponse) {
        
    }

    @Override
    public void onFailure(Exception e) {
        
    }
};

DeleteResponse deleteResponse = client.deleteAsync(deleteResponse, listener);
```

#### DeleteResponse

DeleteResponse 可以检索执行操作的信息

```java
String index = deleteResponse.getIndex();
String type = deleteResponse.getType();
String id = deleteResponse.getId();
long version = deleteResponse.getVersion();
ReplicationResponse.ShardInfo shardInfo = deleteResponse.getShardInfo();
if (shardInfo.getTotal() != shardInfo.getSuccessful()) {
    // 成功分片数目小于总分片
}
if (shardInfo.getFailed() > 0) {
    for (ReplicationResponse.ShardInfo.Failure failure : shardInfo.getFailures()) {
        String reason = failure.reason(); // 处理潜在失败
    }
}
```

### Update API

#### UpdateRequest

UpdateRequest 必须传入下面参数：

- Index
- Type
- Document id

```java
UpdateRequest updateRequest = new DeleteRequest(
        "posts",   // index 
        "doc",     // doc
        "1");      // document id
```

和 index api 类似，UpdateRequest 也支持四种文档格式：

1. json

```java
UpdateRequest updateRequest = new UpdateRequest("posts", "doc", "1");
String jsonString = "{" +
        "\"updated\":\"2017-01-01\"," +
        "\"reason\":\"daily update\"" +
        "}";
request.doc(jsonString, XContentType.JSON); 
```

1. map

```java
Map<String, Object> jsonMap = new HashMap<>();
jsonMap.put("updated", new Date());
jsonMap.put("reason", "daily update");
UpdateRequest updateRequest = new UpdateRequest("posts", "doc", "1")
        .doc(jsonMap); 
```

1. XContentBuilder

```java
XContentBuilder builder = XContentFactory.jsonBuilder();
builder.startObject();
{
    builder.timeField("updated", new Date());
    builder.field("reason", "daily update");
}
builder.endObject();
UpdateRequest updateRequest = new UpdateRequest("posts", "doc", "1")
        .doc(builder);  
```

1. object 键值对

```java
UpdateRequest updateRequest = new UpdateRequest("posts", "doc", "1")
        .doc("updated", new Date(),
             "reason", "daily update"); 
```

可选参数：

1. 超时时间

```java
updateRequest.timeout(TimeValue.timeValueSeconds(1)); 
updateRequest.timeout("1s"); 
```

1. 刷新策略

```java
updateRequest.setRefreshPolicy(WriteRequest.RefreshPolicy.WAIT_UNTIL); 
updateRequest.setRefreshPolicy("wait_for");  
```

1. 冲突后重试次数

```java
updateRequest.retryOnConflict(3);
```

1. 获取数据源，默认是开启的

```java
updateRequest.fetchSource(true); 
```

1. 包括特定字段

```java
String[] includes = new String[]{"updated", "r*"};
String[] excludes = Strings.EMPTY_ARRAY;
updateRequest.fetchSource(new FetchSourceContext(true, includes, excludes)); 
```

1. 排除特定字段

```java
String[] includes = Strings.EMPTY_ARRAY;
String[] excludes = new String[]{"updated"};
updateRequest.fetchSource(new FetchSourceContext(true, includes, excludes)); 
```

1. 指定版本

```java
updateRequest.version(2); 
```

1. 禁用 noop detection

```java
updateRequest.scriptedUpsert(true); 
```

1. 设置如果更新的文档不存在，就必须要创建一个

```java
updateRequest.docAsUpsert(true); 
```

#### 执行

同步执行：

```java
UpdateResponse updateResponse = client.update(updateRequest);
```

异步执行：

```java
ActionListener<UpdateResponse> listener = new ActionListener<UpdateResponse>() {
    @Override
    public void onResponse(UpdateResponse updateResponse) {
        
    }

    @Override
    public void onFailure(Exception e) {
        
    }
};

UpdateResponse updateResponse = client.updateAsync(request, listener); 
```

#### UpdateResponse

```java
String index = updateResponse.getIndex();
String type = updateResponse.getType();
String id = updateResponse.getId();
long version = updateResponse.getVersion();
if (updateResponse.getResult() == DocWriteResponse.Result.CREATED) {
    // 文档已创建
} else if (updateResponse.getResult() == DocWriteResponse.Result.UPDATED) {
    // 文档已更新
} else if (updateResponse.getResult() == DocWriteResponse.Result.DELETED) {
    // 文档已删除
} else if (updateResponse.getResult() == DocWriteResponse.Result.NOOP) {
    // 文档不受更新的影响
}
```

如果在 UpdateRequest 中设置了获取源数据，响应中则包含了更新后的源文档信息：

```java
GetResult result = updateResponse.getGetResult(); 
if (result.isExists()) {
    String sourceAsString = result.sourceAsString();  // 将获取的文档以 string 格式输出
    Map<String, Object> sourceAsMap = result.sourceAsMap(); // 以 Map 格式输出
    byte[] sourceAsBytes = result.source();  // 字节形式
} else {
    // 默认情况下，不会返回文档源数据
}
```

检测是否分片失败：

```java
ReplicationResponse.ShardInfo shardInfo = updateResponse.getShardInfo();
if (shardInfo.getTotal() != shardInfo.getSuccessful()) {
    // 成功的分片数量小于总分片数量
}
if (shardInfo.getFailed() > 0) {
    for (ReplicationResponse.ShardInfo.Failure failure : shardInfo.getFailures()) {
        String reason = failure.reason(); // 得到分片失败的原因
    }
}
```

### Bulk API 批量处理

#### BulkRequest 批量请求

使用 BulkRequest 可以在一次请求中执行多个索引，更新和删除的操作:

```java
BulkRequest request = new BulkRequest();  
request.add(new IndexRequest("posts", "doc", "1")  
        .source(XContentType.JSON,"field", "foo")); // 将第一个 IndexRequest 添加到批量请求中
request.add(new IndexRequest("posts", "doc", "2")  
        .source(XContentType.JSON,"field", "bar")); // 第二个
request.add(new IndexRequest("posts", "doc", "3")  
        .source(XContentType.JSON,"field", "baz")); // 第三个
```

在同一个 BulkRequest 也可以添加不同的操作类型:

```java
BulkRequest bulkRequest = new BulkRequest();
bulkRequest.add(new DeleteRequest("posts", "doc", "3")); 
bulkRequest.add(new UpdateRequest("posts", "doc", "2") 
        .doc(XContentType.JSON,"other", "test"));j
bulkRequest.add(new IndexRequest("posts", "doc", "4")  
        .source(XContentType.JSON,"field", "baz"));
```

可选参数：

1. 超时时间

```java
bulkRequest.timeout(TimeValue.timeValueMinutes(2)); 
bulkRequest.timeout("2m"); 
```

1. 刷新策略

```java
bulkRequest.setRefreshPolicy(WriteRequest.RefreshPolicy.WAIT_UNTIL); 
bulkRequest.setRefreshPolicy("wait_for"); 
```

1. 设置在批量操作前必须有几个分片处于激活状态

```java
bulkRequest.waitForActiveShards(2); 
bulkRequest.waitForActiveShards(ActiveShardCount.ALL);  // 全部分片都处于激活状态
bulkRequest.waitForActiveShards(ActiveShardCount.DEFAULT);  // 默认
bulkRequest.waitForActiveShards(ActiveShardCount.ONE);  // 一个
```

#### 执行

同步请求：

```java
BulkResponse bulkResponse = client.bulk(request);
```

异步请求：

```java
ActionListener<BulkResponse> listener = new ActionListener<BulkResponse>() {
    @Override
    public void onResponse(BulkResponse bulkResponse) {
        
    }

    @Override
    public void onFailure(Exception e) {
        
    }
};

BulkResponse bulkResponse = client.bulkAsync(request, listener); 
```

#### BulkResponse

BulkResponse 中包含执行操作后的信息，并允许对每个操作结果迭代

```java
for (BulkItemResponse bulkItemResponse : bulkResponse) { // 遍历所有的操作结果
    DocWriteResponse itemResponse = bulkItemResponse.getResponse(); // 获取操作结果的响应，可以是  IndexResponse, UpdateResponse or DeleteResponse, 它们都可以惭怍是 DocWriteResponse 实例

    if (bulkItemResponse.getOpType() == DocWriteRequest.OpType.INDEX
            || bulkItemResponse.getOpType() == DocWriteRequest.OpType.CREATE) { 
        IndexResponse indexResponse = (IndexResponse) itemResponse; // index 操作后的响应结果

    } else if (bulkItemResponse.getOpType() == DocWriteRequest.OpType.UPDATE) { 
        UpdateResponse updateResponse = (UpdateResponse) itemResponse; // update 操作后的响应结果

    } else if (bulkItemResponse.getOpType() == DocWriteRequest.OpType.DELETE) { 
        DeleteResponse deleteResponse = (DeleteResponse) itemResponse; // delete 操作后的响应结果
    }
}
```

此外，批量响应还有一个非常便捷的方法来检测是否有一个或多个操作失败

```java
if (bulkResponse.hasFailures()) { // 表示至少有一个操作失败
    // 遍历所有的操作结果，检查是否是失败的操作，并获取对应的失败信息
	for (BulkItemResponse bulkItemResponse : bulkResponse) {
        if (bulkItemResponse.isFailed()) { // 检测给定的操作是否失败
            BulkItemResponse.Failure failure = bulkItemResponse.getFailure(); // 获取失败信息
        }
    }
}
```

#### BulkProcessor

BulkProcessor 是为了简化 Bulk API 的操作提供的一个工具类，要执行操作，就需要下面组件:

- RestHighLevelClient 用来执行 BulkRequest 并获取 BulkResponse
- BulkProcessor.Listener 对 BulkRequest 执行前后以及失败时监听

BulkProcessor.builder 方法用来构建一个新的 BulkProcessor：

```java
ulkProcessor.Listener listener = new BulkProcessor.Listener() { 
    @Override
    public void beforeBulk(long executionId, BulkRequest request) {
        // 在每个 BulkRequest 执行前调用
    }

    @Override
    public void afterBulk(long executionId, BulkRequest request,
            BulkResponse response) {
        // 在每个 BulkRequest 执行后调用
    }

    @Override
    public void afterBulk(long executionId, BulkRequest request, Throwable failure) {
        // 失败时调用
    }
};

BulkProcessor bulkProcessor =
        BulkProcessor.builder(client::bulkAsync, listener).build(); // 构建 BulkProcessor, RestHighLevelClient.bulkAsync()  用来执行 BulkRequest 
```

BulkProcessor.Builder 提供了多个方法来配置 BulkProcessor 如何来处理请求的执行:

```java
BulkProcessor.Builder builder = BulkProcessor.builder(client::bulkAsync, listener);
builder.setBulkActions(500); // 指定多少操作时，就会刷新一次
builder.setBulkSize(new ByteSizeValue(1L, ByteSizeUnit.MB)); 
builder.setConcurrentRequests(0);  // 指定多大容量，就会刷新一次
builder.setFlushInterval(TimeValue.timeValueSeconds(10L)); // 允许并发执行的数量 
builder.setBackoffPolicy(BackoffPolicy
        .constantBackoff(TimeValue.timeValueSeconds(1L), 3)); 
```

BulkProcessor 创建后，各种请求就可以添加进去：

```java
IndexRequest one = new IndexRequest("posts", "doc", "1").
        source(XContentType.JSON, "title",
                "In which order are my Elasticsearch queries executed?");
IndexRequest two = new IndexRequest("posts", "doc", "2")
        .source(XContentType.JSON, "title",
                "Current status and upcoming changes in Elasticsearch");
IndexRequest three = new IndexRequest("posts", "doc", "3")
        .source(XContentType.JSON, "title",
                "The Future of Federated Search in Elasticsearch");

bulkProcessor.add(one);
bulkProcessor.add(two);
bulkProcessor.add(three);
```

BulkProcessor 执行时，会对每个 bulk request调用 BulkProcessor.Listener ， listener 提供了下面方法来访问 BulkRequest 和 BulkResponse:

```java
BulkProcessor.Listener listener = new BulkProcessor.Listener() {
    @Override
    public void beforeBulk(long executionId, BulkRequest request) {
        int numberOfActions = request.numberOfActions(); // 在执行前获取操作的数量
        logger.debug("Executing bulk [{}] with {} requests",
                executionId, numberOfActions);
    }

    @Override
    public void afterBulk(long executionId, BulkRequest request,
            BulkResponse response) {
        if (response.hasFailures()) { // 执行后查看响应中是否包含失败的操作
            logger.warn("Bulk [{}] executed with failures", executionId);
        } else {
            logger.debug("Bulk [{}] completed in {} milliseconds",
                    executionId, response.getTook().getMillis());
        }
    }

    @Override
    public void afterBulk(long executionId, BulkRequest request, Throwable failure) {
        logger.error("Failed to execute bulk", failure); // 请求失败时打印信息
    }
};
```

请求添加到 BulkProcessor ， 它的实例可以使用下面两种方法关闭请求：

1. awaitClose() 在请求返回后或等待一定时间关闭

```java
boolean terminated = bulkProcessor.awaitClose(30L, TimeUnit.SECONDS); 
```

1. close() 立刻关闭

```java
bulkProcessor.close();
```

两个方法都会在关闭前对处理器中的请求进行刷新，并避免新的请求添加进去。

### Multi-Get API

multiGet API 可以在单个 http 交互中并行的执行多个 get 请求。

#### MultiGetRequest

MultiGetRequest 实例化时参数为空，实例化后可以通过添加 MultiGetRequest.Item 来配置获取的信息

```java
MultiGetRequest request = new MultiGetRequest();
request.add(new MultiGetRequest.Item(
    "index",     // 索引  
    "type",      // 类型
    "example_id"));  // 文档 idj
request.add(new MultiGetRequest.Item("index", "type", "another_id"));  // 添加另外一个条目
```

可选参数：

与前面 Get API 可选参数相同

#### 执行

同步执行：

```java
MultiGetResponse response = client.multiGet(request);
```

异步执行：

```java
ActionListener<MultiGetResponse> listener = new ActionListener<MultiGetResponse>() {
    @Override
    public void onResponse(MultiGetResponse response) {
        
    }

    @Override
    public void onFailure(Exception e) {
        
    }
};

client.multiGetAsync(request, listener); 
```

#### MultiGetResponse

MultiGetResponse 中getResponse 方法包含的 MultiGetItemResponse 顺序与请求时的相 MultiGetItemResponse ，如果执行成功，就会返回 GetResponse 对象，失败则返回 MultiGetResponse.Failure

```java
MultiGetItemResponse firstItem = response.getResponses()[0];
assertNull(firstItem.getFailure());     // 执行成功，则返回 null         
GetResponse firstGet = firstItem.getResponse();  // 返回 GetResponse 对象
String index = firstItem.getIndex();
String type = firstItem.getType();
String id = firstItem.getId();
if (firstGet.isExists()) {
    long version = firstGet.getVersion();
    String sourceAsString = firstGet.getSourceAsString();  // string 格式      
    Map<String, Object> sourceAsMap = firstGet.getSourceAsMap(); // Map 
    byte[] sourceAsBytes = firstGet.getSourceAsBytes();       // bytes   
} else {
    // 没有发现文档
    // 尽管响应中会返回 404 状态码，也会返回一个有效的 GetResponse
    // 这是可以使用 isExists 方法来判断
}
```

如果子请求中对应的 index 不存在，返回的响应中的getFailure 方法中会包含 exception:

```java
assertNull(missingIndexItem.getResponse());    // 获取的响应为空            
Exception e = missingIndexItem.getFailure().getFailure();  // 获取 exception
ElasticsearchException ee = (ElasticsearchException) e;    
// TODO status is broken! fix in a followup
// assertEquals(RestStatus.NOT_FOUND, ee.status());        
assertThat(e.getMessage(),
    containsString("reason=no such index"));    
```

## 查询（Search）API

Java High Level REST Client 支持下面的 Search API：

- Search API
- Search Scroll API
- Clear Scroll API
- Multi-Search API
- Ranking Evaluation API

### Search API

#### SearchRequest

searchRequest 用来完成和搜索文档，聚等相关的操作同时也提供了各种方式来完成对查询结果的高亮操作。

最基本的查询操作如下:

```java
SearchRequest searchRequest = new SearchRequest(); 
SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder(); 
searchSourceBuilder.query(QueryBuilders.matchAllQuery()); // 添加 match_all 查询
searchRequest.source(searchSourceBuilder); // 将 SearchSourceBuilder  添加到 SeachRequest 中
```

可选参数:

```java
SearchRequest searchRequest = new SearchRequest("posts");  // 设置搜索的 index
searchRequest.types("doc");  // 设置搜索的 type
searchRequest.routing("routing"); // 设置 routing 参数
searchRequest.preference("_local");  // 配置搜索时偏爱使用本地分片，默认是使用随机分片
```

##### SearchSourceBuilder

对搜索行为的配置可以使用 SearchSourceBuilder 来完成:

```java
SearchSourceBuilder sourceBuilder = new SearchSourceBuilder();  // 默认配置
sourceBuilder.query(QueryBuilders.termQuery("user", "kimchy")); // 设置搜索，可以是任何类型的 QueryBuilder
sourceBuilder.from(0); // 起始 index
sourceBuilder.size(5); // 大小 size
sourceBuilder.timeout(new TimeValue(60, TimeUnit.SECONDS)); // 设置搜索的超时时间

SearchRequest searchRequest = new SearchRequest();
searchRequest.source(sourceBuilder);
```

**SearchSourceBuilder 可选配置有：**

##### 1. 构建查询条件

查询请求是通过使用 QueryBuilder 对象来完成的，并且支持 Query DSL（领域特定语言，是指专注于某个应用程序领域的计算机语言）。

使用构造函数来创建 QueryBuilder：

```java
MatchQueryBuilder matchQueryBuilder = new MatchQueryBuilder("user", "kimchy"); 

// 配置查询选项
matchQueryBuilder.fuzziness(Fuzziness.AUTO);  // 模糊查询
matchQueryBuilder.prefixLength(3); // 前缀查询的长度
matchQueryBuilder.maxExpansions(10); // max expansion 选项，用来控制模糊查询
```

也可以使用QueryBuilders 工具类来创建 QueryBuilder 对象。这个类提供了函数式编程风格的各种方法用来快速创建 QueryBuilder 对象。

```java
QueryBuilder matchQueryBuilder = QueryBuilders.matchQuery("user", "kimchy")
                                        .fuzziness(Fuzziness.AUTO)
                                                .prefixLength(3)
                                                .maxExpansions(10);
```

最后要添加到 `SearchSourceBuilder` 中:

```java
searchSourceBuilder.query(matchQueryBuilder);
```

##### 2. 指定排序

SearchSourceBuilder 允许添加一个或多个SortBuilder 实例。这里包含 4 种特殊的实现, (Field-, Score-, GeoDistance- 和 ScriptSortBuilder)

```java
sourceBuilder.sort(new ScoreSortBuilder().order(SortOrder.DESC)); // 根据分数 _score 降序排列 (默认行为)
sourceBuilder.sort(new FieldSortBuilder("_uid").order(SortOrder.ASC));  // 根据 id 降序排列
```

##### 3. 过滤数据源

默认情况下，查询请求会返回文档的内容 _source ,当然我们也可以配置它。例如，禁止对 _source 的获取

```java
sourceBuilder.fetchSource(false);
```

也可以使用通配符模式以更细的粒度包含或排除特定的字段:

```java
String[] includeFields = new String[] {"title", "user", "innerObject.*"};
String[] excludeFields = new String[] {"_type"};
sourceBuilder.fetchSource(includeFields, excludeFields);
```

##### 4. 高亮请求

可以通过在 SearchSourceBuilder 上设置 HighlightBuilder 完成对结果的高亮，而且可以配置不同的字段具有不同的高亮行为。

```java
SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
HighlightBuilder highlightBuilder = new HighlightBuilder(); 
HighlightBuilder.Field highlightTitle =
        new HighlightBuilder.Field("title"); // title 字段高亮
highlightTitle.highlighterType("unified");  // 配置高亮类型
highlightBuilder.field(highlightTitle);  // 添加到 builder
HighlightBuilder.Field highlightUser = new HighlightBuilder.Field("user");
highlightBuilder.field(highlightUser);
searchSourceBuilder.highlighter(highlightBuilder);
```

##### 5. 聚合请求

要实现聚合请求分两步

1. 创建合适的 `AggregationBuilder`
2. 作为参数配置在 `SearchSourceBuilder`

```java
SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
TermsAggregationBuilder aggregation = AggregationBuilders.terms("by_company")
        .field("company.keyword");
aggregation.subAggregation(AggregationBuilders.avg("average_age")
        .field("age"));
searchSourceBuilder.aggregation(aggregation);
```

##### 6. 建议请求 Requesting Suggestions

SuggestionBuilder 实现类是由 SuggestBuilders 工厂类来创建的。

```java
SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
SuggestionBuilder termSuggestionBuilder =
    SuggestBuilders.termSuggestion("user").text("kmichy"); 
SuggestBuilder suggestBuilder = new SuggestBuilder();
suggestBuilder.addSuggestion("suggest_user", termSuggestionBuilder); 
searchSourceBuilder.suggest(suggestBuilder);
```

##### 7. 对请求和聚合分析

分析 API 可用来对一个特定的查询操作中的请求和聚合进行分析，此时要将SearchSourceBuilder 的 profile标志位设置为 true

```java
SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
searchSourceBuilder.profile(true);
```

#### 执行

同步执行

同步执行是阻塞式的，只有结果返回后才能继续执行

```java
SearchResponse searchResponse = client.search(searchRequest);
```

异步执行

异步执行使用的是 listener 对结果进行处理

```java
ActionListener<SearchResponse> listener = new ActionListener<SearchResponse>() {
    @Override
    public void onResponse(SearchResponse searchResponse) {
        // 查询成功
    }

    @Override
    public void onFailure(Exception e) {
        // 查询失败
    }
};

SearchResponse searchResponse = client.search(searchRequest);
```

#### SearchResponse

查询执行完成后，会返回 SearchResponse 对象，并在对象中包含查询执行的细节和符合条件的文档集合。

SerchResponse 包含的信息如下：

- 请求本身的信息，如 HTTP 状态码，执行时间，或者请求是否超时

```java
RestStatus status = searchResponse.status(); // HTTP 状态码
TimeValue took = searchResponse.getTook(); // 查询占用的时间
Boolean terminatedEarly = searchResponse.isTerminatedEarly(); // 是否由于 SearchSourceBuilder 中设置 terminateAfter 而过早终止
boolean timedOut = searchResponse.isTimedOut(); // 是否超时
```

- 查询影响的分片数量的统计信息，成功和失败的分片

```java
int totalShards = searchResponse.getTotalShards();
int successfulShards = searchResponse.getSuccessfulShards();
int failedShards = searchResponse.getFailedShards();
for (ShardSearchFailure failure : searchResponse.getShardFailures()) {
    // failures should be handled here
}
```

- SearchHits

```java
SearchHits hits = searchResponse.getHits();

long totalHits = hits.getTotalHits();
float maxScore = hits.getMaxScore();
SearchHit[] searchHits = hits.getHits();
for (SearchHit hit : searchHits) {
    // do something with the SearchHit
    String index = hit.getIndex();
    String type = hit.getType();
    String id = hit.getId();
    float score = hit.getScore();
    
    // 获取文档源数据
    String sourceAsString = hit.getSourceAsString();
    Map<String, Object> sourceAsMap = hit.getSourceAsMap();
    String documentTitle = (String) sourceAsMap.get("title");
    List<Object> users = (List<Object>) sourceAsMap.get("user");
    Map<String, Object> innerObject =
            (Map<String, Object>) sourceAsMap.get("innerObject");
}
```