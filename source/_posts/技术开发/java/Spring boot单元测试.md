---
title: Spring boot单元测试
date: 2022-12-15 23:12:12
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - Spring boot单元测试
---
公司职级认证有单元测试要求，花了一天时间把欠下的的补完了。。。

#### spring boot引入单元测试

pom.xml 文件中写入：

```java
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

spring boot中单元测试目录与main同级

#### spring boot使用单元测试

1. 快捷生成测试类
   idea 中选中要测试的类 -> Ctrl+Shift+T 打开创建测试类窗口 -> 选择要测试的方法，创建测试类 生成的类路径为 Test 包下的同名路径。
2. 自己创建测试类
   Test 目录下自己创建类。。。

类创建完成后还需要加上注解，如下：

```java
@RunWith(SpringRunner.class)
@SpringBootTest
public class myServiceTest {

    @Test
    public void test(){
      //...
    }
}
```

#### 不同场景下的单元测试

1. 对于 Controller 层单元测试，使用 @AutoConfigureMockMvc，示例代码如下：

```java
@RunWith(SpringRunner.class)
@SpringBootTest
@AutoConfigureMockMvc
public class LicenseInfoResourceTest extends AbstractRestControllerTest {
    /**
     * 初始化MockMvc
     */
    @Autowired
    private MockMvc mvc;

    /**
     * 测试的controller
     */
    @MockBean
    private LicenseInfoResource licenseInfoResource;

    @Before
    public void setUp() {
        SecurityContextHolder.clearContext();
    }

    @Test
    @WithMockUser(username = "admin", password = "admin")
    public void getLicenseInfo() throws Exception {

        MvcResult mvcResult = mvc.perform(MockMvcRequestBuilders.get("/license/get_platform_info"))
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andDo(MockMvcResultHandlers.print())
                .andReturn();
        System.out.println("content" + mvcResult.getResponse().getContentAsString());
    }
}
```

1. 对于有运行时环境的要求，当前用户记录等，需要在类或者方法上加上注册变量：

```
@WithMockUser(username = "admin", password = "admin")
```

1. 对于单点登陆应用，调用接口需要 token ,可以先获取token，然后加入到请求头中：

```java
/* 获取token工具类 */
public final class LogInUtils {

   private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

   private LogInUtils() {
   }

   public static String getTokenForLogin(String username, String password, MockMvc mockMvc) throws Exception {
      // 设置验证码
      MockHttpSession session = new MockHttpSession();
      session.setAttribute("vrifyCode", "123456");
      String code = "123456";

      String content = mockMvc.perform(post("/api/authenticate")
         .contentType(MediaType.APPLICATION_JSON)
         .session(session)
         .content("{\"password\": \"" + password + "\", \"username\": \"" + username + "\", \"code\": \""+ code + "\"}"))
         .andReturn()
         .getResponse()
         .getContentAsString();
      AuthenticationResponse authResponse = OBJECT_MAPPER.readValue(content, AuthenticationResponse.class);

      return authResponse.getIdToken();
   }

   private static class AuthenticationResponse {

      @JsonAlias("id_token")
      private String idToken;

      public void setIdToken(String idToken) {
         this.idToken = idToken;
      }

      public String getIdToken() {
         return idToken;
      }
   }
}
/* 获取token加入到请求头 */
@Test
public void createRole() throws Exception {
    final String token = LogInUtils.getTokenForLogin("admin", "admin", mvc);

    String json = "{\"name\":\"超级管理员2\",\"remark\":\"权限\",\"permissionIds\":\"1\"}";

    MvcResult mvcResult = mvc.perform(MockMvcRequestBuilders.post("/role/create_role")
            .contentType(MediaType.APPLICATION_JSON)
            .content(json)
            .header("Authorization", "Bearer " + token))
            .andExpect(MockMvcResultMatchers.status().isOk())
            .andDo(MockMvcResultHandlers.print())
            .andReturn();
    System.out.println("status: " + mvcResult.getResponse().getStatus());
}
```

#### MocMvc详解

转载自 https://blog.csdn.net/wo541075754/article/details/88983708

1. 什么是Mock?
   模拟对象（mock object），是以可控的方式模拟真实对象行为的假对象。在编程过程中，通常通过模拟一些输入数据，来验证程序是否达到预期结果。使用模拟对象，可以模拟复杂的、真实的对象行为。如果在单元测试中无法使用真实对象，可采用模拟对象进行替代。
2. 什么是MockMvc？
   MockMvc是由spring-test包提供，实现了对Http请求的模拟，能够直接使用网络的形式，转换到Controller的调用，使得测试速度快、不依赖网络环境。同时提供了一套验证的工具，结果的验证十分方便。
3. spring使用MocMvc
   spring中使用MockMvcBuilder来构造MocMvc。它有两种实现方式：StandaloneMockMvcBuilder和DefaultMockMvcBuilder，分别对应两种测试方式，即独立安装和集成Web环境测试（并不会集成真正的web环境，而是通过相应的Mock API进行模拟测试，无须启动服务器）。
   代码示例：

```java
//SpringBoot1.4版本之前用的是SpringJUnit4ClassRunner.class
@RunWith(SpringRunner.class)
//SpringBoot1.4版本之前用的是@SpringApplicationConfiguration(classes = Application.class)
@SpringBootTest
//测试环境使用，用来表示测试环境使用的ApplicationContext将是WebApplicationContext类型的
@WebAppConfiguration
public class HelloWorldTest {

	private MockMvc mockMvc;

	@Autowired
	private WebApplicationContext webApplicationContext;

	@Before
	public void setup() {
		// 实例化方式一
		mockMvc = MockMvcBuilders.standaloneSetup(new HelloWorldController()).build();
		// 实例化方式二
//		mockMvc = MockMvcBuilders.webAppContextSetup(webApplicationContext).build();
	}
```

单元测试方法：

```java
@Test
public void testHello() throws Exception {

	/*
	 * 1、mockMvc.perform执行一个请求。
	 * 2、MockMvcRequestBuilders.get("XXX")构造一个请求。
	 * 3、ResultActions.param添加请求传值
	 * 4、ResultActions.accept(MediaType.TEXT_HTML_VALUE))设置返回类型
	 * 5、ResultActions.andExpect添加执行完成后的断言。
	 * 6、ResultActions.andDo添加一个结果处理器，表示要对结果做点什么事情
	 *   比如此处使用MockMvcResultHandlers.print()输出整个响应结果信息。
	 * 7、ResultActions.andReturn表示执行完成后返回相应的结果。
	 */
	mockMvc.perform(MockMvcRequestBuilders
			.get("/hello")
			// 设置返回值类型为utf-8，否则默认为ISO-8859-1
			.accept(MediaType.APPLICATION_JSON_UTF8_VALUE)
			.param("name", "Tom"))
			.andExpect(MockMvcResultMatchers.status().isOk())
			.andExpect(MockMvcResultMatchers.content().string("Hello Tom!"))
			.andDo(MockMvcResultHandlers.print());
}
```

整个过程如下：

```
1、准备测试环境
2、通过MockMvc执行请求
3、添加验证断言
4、添加结果处理器
5、得到MvcResult进行自定义断言/进行下一步的异步请求
6、卸载测试环境
```

Sping boot2.0后使用MocMvc更加方便，只需要在测试类加上`@AutoConfigureMockMvc`注解，就可以注入MocMvc:

```java
@RunWith(SpringRunner.class)
@SpringBootTest
@AutoConfigureMockMvc
public class  Test  {
    /**
     * 初始化MockMvc
     */
    @Autowired
    private MockMvc mvc;
    
    //...
}
```

注意事项：如果使用DefaultMockMvcBuilder进行MockMvc实例化时需在SpringBoot启动类上添加组件扫描的package的指定，否则会出现404。如：

```java
@ComponentScan(basePackages = "com.secbro2")
```

#### 一些常用的测试

1. 测试普通控制器

```java
mockMvc.perform(get("/user/{id}", 1)) //执行请求  
            .andExpect(model().attributeExists("user")) //验证存储模型数据  
            .andExpect(view().name("user/view")) //验证viewName  
            .andExpect(forwardedUrl("/WEB-INF/jsp/user/view.jsp"))//验证视图渲染时forward到的jsp  
            .andExpect(status().isOk())//验证状态码  
            .andDo(print()); //输出MvcResult到控制台
```

1. 得到MvcResult自定义验证

```
MvcResult result = mockMvc.perform(get("/user/{id}", 1))//执行请求  
        .andReturn(); //返回MvcResult  
Assert.assertNotNull(result.getModelAndView().getModel().get("user")); //自定义断言 
```

1. 验证请求参数绑定到模型数据及Flash属性

```java
mockMvc.perform(post("/user").param("name", "zhang")) //执行传递参数的POST请求(也可以post("/user?name=zhang"))  
            .andExpect(handler().handlerType(UserController.class)) //验证执行的控制器类型  
            .andExpect(handler().methodName("create")) //验证执行的控制器方法名  
            .andExpect(model().hasNoErrors()) //验证页面没有错误  
            .andExpect(flash().attributeExists("success")) //验证存在flash属性  
            .andExpect(view().name("redirect:/user")); //验证视图  
```

1. 文件上传

```
byte[] bytes = new byte[] {1, 2};  
mockMvc.perform(fileUpload("/user/{id}/icon", 1L).file("icon", bytes)) //执行文件上传  
        .andExpect(model().attribute("icon", bytes)) //验证属性相等性  
        .andExpect(view().name("success")); //验证视图 
```

1. JSON请求/响应验证

```java
String requestBody = "{\"id\":1, \"name\":\"zhang\"}";  
    mockMvc.perform(post("/user")  
            .contentType(MediaType.APPLICATION_JSON).content(requestBody)  
            .accept(MediaType.APPLICATION_JSON)) //执行请求  
            .andExpect(content().contentType(MediaType.APPLICATION_JSON)) //验证响应contentType  
            .andExpect(jsonPath("$.id").value(1)); //使用Json path验证JSON 请参考http://goessner.net/articles/JsonPath/  
      
    String errorBody = "{id:1, name:zhang}";  
    MvcResult result = mockMvc.perform(post("/user")  
            .contentType(MediaType.APPLICATION_JSON).content(errorBody)  
            .accept(MediaType.APPLICATION_JSON)) //执行请求  
            .andExpect(status().isBadRequest()) //400错误请求  
            .andReturn();  
      
    Assert.assertTrue(HttpMessageNotReadableException.class.isAssignableFrom(result.getResolvedException().getClass()));//错误的请求内容体
```

1. 异步测试

```java
//Callable  
    MvcResult result = mockMvc.perform(get("/user/async1?id=1&name=zhang")) //执行请求  
            .andExpect(request().asyncStarted())  
            .andExpect(request().asyncResult(CoreMatchers.instanceOf(User.class))) //默认会等10秒超时  
            .andReturn();  
      
    mockMvc.perform(asyncDispatch(result))  
            .andExpect(status().isOk())  
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))  
            .andExpect(jsonPath("$.id").value(1));  
//Callable  
    MvcResult result = mockMvc.perform(get("/user/async1?id=1&name=zhang")) //执行请求  
            .andExpect(request().asyncStarted())  
            .andExpect(request().asyncResult(CoreMatchers.instanceOf(User.class))) //默认会等10秒超时  
            .andReturn();  
      
    mockMvc.perform(asyncDispatch(result))  
            .andExpect(status().isOk())  
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))  
            .andExpect(jsonPath("$.id").value(1));  
```

1. 全局配置

```java
mockMvc = webAppContextSetup(wac)  
            .defaultRequest(get("/user/1").requestAttr("default", true)) //默认请求 如果其是Mergeable类型的，会自动合并的哦mockMvc.perform中的RequestBuilder  
            .alwaysDo(print())  //默认每次执行请求后都做的动作  
            .alwaysExpect(request().attribute("default", true)) //默认每次执行后进行验证的断言  
            .build();  
      
    mockMvc.perform(get("/user/1"))  
            .andExpect(model().attributeExists("user"));
```