转载自 [spring-security-4介绍](https://www.cnblogs.com/wutianqi/p/9174227.html)

虽然现在已经到了5.x版本了，但是大同小异，知识还是不会过时的。。。


## 前言
本教程主要分为个部分：
- spring security Java配置的搭建
- spring security过滤器的创建与注册原理
- spring security Java配置搭建中认证与授权的分析
- spring security Java配置实现自定义的表单认证与授权

这篇教程主要是用来教会你以下几点：
- 怎么搭建spring security
- spring secuirty过滤器的创建与注册原理（工作的基本原理）
- 简单的认证与授权的原理
- 在明白如何实现简单的认证与授权的基础上实现自定义的认证与授权

环境说明：
- 版本：本教程使用的spring security版本是4.2.3.RELEASE，对应的spring版本是4.3.11.RELEASE。
- 工具：开发工具为eclipse，构建工具为maven

## 一、什么是spring security?
spring security是基于spring开发的为JavaEE企业级应用提供安全服务的框架。安全服务主要是指 认证（Authentication）和 授权（Authorization）。

## 二、spring security的模块
　搭建spring security首先我们要导入必须的jar，即maven的依赖。spring security按模块划分，一个模块对应一个jar。

spring security分为以下九个模块：

　　　　1. Core spring-security-core.jar：核心模块。包含核心的认证（authentication）和授权（authorization）的类和接口，远程支持和基础配置API。

　　　　2. Remoting spring-security-remoting.jar：提供与spring remoting整合的支持。

　　　　3. Web spring-security-web.jar：包含过滤器和相关的网络安全的代码。用于我们进行web安全验证和基于URL的访问控制。

　　　　4. Config spring-security-config.jar：包含security namepace的解析代码。

　　　　5. LDAP spring-security-ldap.jar：提供LDAP验证和配置的支持。

　　　　6. ACL spring-security-acl.jar：提供对特定domain对象的ACL（访问控制列表）实现。用来限定对特定对象的访问

　　　　7. CAS sprig-security-cas.jar：提供与spring security CAS客户端集成

　　　　8. OpenID spring-security-openid.jar：提供OpenId Web验证支持。基于一个外部OpenId服务器对用户进行验证。

　　　　9. Test spring-security-test.jar：提供spring security的测试支持。

　　一般情况下，Core和Config模块都是需要的，因为我们本教程只是用于Java web应用表单的验证登录，所以这里我们还需要引入Web。

　　说明：本篇教程的代码已上传github，地址：https://github.com/wutianqi/spring_security_create

## 三、工程搭建
#### 1.项目工程结构
![工程结构](https://note.youdao.com/yws/api/personal/file/3186B9EC554D41A297D00EF2B4FEA930?method=getImage&version=5756&cstk=szLZezq4)

#### 2. 代码展示
2.1 pom.xml
```
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.wuqi</groupId>
  <artifactId>spring_security_create</artifactId>
  <packaging>war</packaging>
  <version>0.0.1-SNAPSHOT</version>
  <name>spring_security_create Maven Webapp</name>
  <url>http://maven.apache.org</url>
  
  <properties>
      <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
      <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
      <!-- web -->
      <jsp.version>2.2</jsp.version>
      <servlet.version>3.1.0</servlet.version>
      <jstl.version>1.2</jstl.version>
      <!-- spring 和 spring security -->
      <spring-security.version>4.2.3.RELEASE</spring-security.version>
      <spring-framework.version>4.3.11.RELEASE</spring-framework.version>
      <!-- Logging -->
      <logback.version>1.0.13</logback.version>
      <slf4j.version>1.7.5</slf4j.version>
  </properties>
  
  <dependencies>
       <!-- spring -->
       <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-webmvc</artifactId>
        <version>${spring-framework.version}</version>
     </dependency>
     <dependency>    
            <groupId>org.springframework</groupId>    
            <artifactId>spring-tx</artifactId>   
            <version>${spring-framework.version}</version> 
     </dependency>
       <!-- spring security -->
     <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-core</artifactId>
        <version>${spring-security.version}</version>
     </dependency>
     <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-web</artifactId>
        <version>${spring-security.version}</version>
     </dependency>
     <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-config</artifactId>
        <version>${spring-security.version}</version>
     </dependency>
    <!-- 其他一些依赖 -->
    <dependency>
      <groupId>javax</groupId>
      <artifactId>javaee-web-api</artifactId>
      <version>7.0</version>
      <scope>provided</scope>
    </dependency>
    <dependency>    
        <groupId>javax.servlet</groupId>    
        <artifactId>javax.servlet-api</artifactId>    
        <version>${servlet.version}</version>    
        <scope>provided</scope>   
    </dependency>    
     <dependency>    
            <groupId>javax.servlet</groupId>    
            <artifactId>jstl</artifactId>    
            <version>${jstl.version}</version> 
     </dependency> 
     <dependency>    
            <groupId>javax.servlet.jsp</groupId>    
            <artifactId>jsp-api</artifactId>    
            <version>${jsp.version}</version> 
            <scope>provided</scope>   
     </dependency>
     <dependency>
          <groupId>com.fasterxml.jackson.dataformat</groupId>
          <artifactId>jackson-dataformat-xml</artifactId>
          <version>2.5.3</version>
     </dependency>
      <!-- 日志 -->
    <!-- 使用SLF4J和LogBack作为日志 --> 
     <dependency>    
         <groupId>org.slf4j</groupId>    
         <artifactId>slf4j-api</artifactId>    
         <version>${slf4j.version}</version>    
     </dependency> 
     <dependency>    
         <groupId>log4j</groupId>    
         <artifactId>log4j</artifactId>    
         <version>1.2.16</version>    
     </dependency> 
     <dependency>    
         <groupId>org.slf4j</groupId>    
         <artifactId>jcl-over-slf4j</artifactId>    
         <version>${slf4j.version}</version>    
     </dependency>
     <!--logback日志-->    
      <dependency>    
          <groupId>ch.qos.logback</groupId>    
          <artifactId>logback-core</artifactId>    
          <version>${logback.version}</version>    
      </dependency>    
      <!--实现slf4j接口并整合-->    
      <dependency>    
          <groupId>ch.qos.logback</groupId>    
          <artifactId>logback-classic</artifactId>    
          <version>${logback.version}</version>    
      </dependency>  
      <dependency>    
          <groupId>ch.qos.logback</groupId>    
          <artifactId>logback-access</artifactId>    
          <version>${logback.version}</version>    
      </dependency>  
  </dependencies>
  <build>
    <finalName>spring_security_create</finalName>
    <plugins>
        <!-- 配置maven的内嵌的tomcat，通过内置的tomcat启动 -->
        <plugin>
            <groupId>org.apache.tomcat.maven</groupId>
            <artifactId>tomcat7-maven-plugin</artifactId>
            <version>2.2</version>
            <configuration>
            <uriEncoding>utf8</uriEncoding>
            <!-- 配置启动的端口为9090 -->
            <port>9090</port>
            <path>/</path>
            </configuration>
         </plugin>
    </plugins>
  </build>
</project>
```
　该pom文件除了包括了spring security的依赖外，还包括了spring、springmvc、日志的一些依赖，除了spring security的依赖，其他的你没必要太过于纠结。直接拿过来用就可以了。日志我使用了logback，这个你也直接拿过来用就行了，直接将logback.xml放在你的类路径下就可以起作用了。而且这些知识也不是本篇教程所讨论的。
　
2.2  MyWebConfig
```java
package com.wuqi.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;
import org.springframework.web.servlet.view.InternalResourceViewResolver;
import org.springframework.web.servlet.view.JstlView;
/**
 * MVC配置类
 * @author wuqi
 * @date 2018/06/13
 */
@EnableWebMvc
@Configuration
@ComponentScan("com.wuqi")
public class MyWebConfig extends WebMvcConfigurerAdapter {

    //配置mvc视图解析器
    @Bean
    public InternalResourceViewResolver viewResolver() {
        InternalResourceViewResolver viewResolver = new InternalResourceViewResolver();
        viewResolver.setPrefix("/WEB-INF/classes/views/");
        viewResolver.setSuffix(".jsp");
        viewResolver.setViewClass(JstlView.class);
        return viewResolver;
    }    
}
```
MyWebConfig是SpringMvc的配置类，这里只配置了视图解析器

2.3 WebInitializer
```java
package com.wuqi.config;

import org.springframework.web.servlet.support.AbstractAnnotationConfigDispatcherServletInitializer;
/**
 * 替代web.xml的配置
 * @author wuqi
 * @date 2018/06/13
 */
public class WebInitializer extends AbstractAnnotationConfigDispatcherServletInitializer {

    @Override
    protected Class<?>[] getRootConfigClasses() {
        return null;
    }

    @Override
    protected Class<?>[] getServletConfigClasses() {
        return new Class[] {MyWebConfig.class};
    }

    @Override
    protected String[] getServletMappings() {
        //将DispatcherServlet映射到 /
        return new String[] {"/"};
    }

}
```
WebInitializer相当于在web.xml中注册DispatcherServlet，以及配置Spring Mvc的配置文件

2.4 MySecurityConfig
```java
package com.wuqi.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
/**
 * spring security配置类
 * @author wuqi
 * @date 2018/06/13
 */
@EnableWebSecurity
@Configuration
public class MySecurityConfig extends WebSecurityConfigurerAdapter {
    
    @Autowired
    public void configUser(AuthenticationManagerBuilder builder) throws Exception {
        builder
            .inMemoryAuthentication()
                //创建用户名为user，密码为password的用户
                .withUser("user").password("password").roles("USER");
    }
    
}
```
MySecurityConfig是spring security的配置类，定制spring security的一些行为就在这里。其中@EnableWebSecurity用于创建过滤器

2.5 SecurityInitializer 
```java
package com.wuqi.config;

import org.springframework.security.web.context.AbstractSecurityWebApplicationInitializer;
/**
 * security初始化类，用户注册过滤器
 * @author wuqi
 * @date 2018/06/13
 */
public class SecurityInitializer extends AbstractSecurityWebApplicationInitializer {

}
```
SecurityInitializer主要就是用于注册spring secuirty的过滤器

2.6 logback.xml
```
<?xml version="1.0" encoding="UTF-8"?>  
<configuration scan="true" scanPeriod="1 seconds">  
    <contextListener class="ch.qos.logback.classic.jul.LevelChangePropagator">
        <resetJUL>true</resetJUL>
    </contextListener>
    <jmxConfigurator />
  <appender name="console" class="ch.qos.logback.core.ConsoleAppender">  
    <encoder>
        <pattern>logbak: %d{HH:mm:ss.SSS} %logger{36} - %msg%n</pattern>
    </encoder> 
  </appender>  
  
  <logger name="org.springframework.security.web" level="DEBUG" />  
  <logger name="org.springframework.security" level="DEBUG" />  
  <logger name="org.springframework.security.config" level="DEBUG" />  
  
  <root level="INFO">  
    <appender-ref ref="console" />  
  </root>  
</configuration>
```
该日志文件就是将web、core、config模块的日志级别调为debug模式。

#### 3. 运行展示
3.1 通过maven内置的Tomcat启动项目（不知道的网上看下，有很多资料），访问端口为9090。地址栏访问  http://localhost:9090

![运行展示1](https://note.youdao.com/yws/api/personal/file/4C189F378ED642D29B1CFEB7E0710953?method=getImage&version=5821&cstk=szLZezq4)

由此可以看到当访问我们的项目时，spring security将我们的项目保护了起来，并提供了一个默认的登录页面，让我们去登录。我们在MySecurityConfig中配置了一个用户。用户名为"user"，密码为"password"，输入这个用户名和密码，即可正常访问我们的项目。

3.2 输入用户名和密码

![运行展示2](https://note.youdao.com/yws/api/personal/file/024CBDB6050549E2AEE13B3AB7C3D507?method=getImage&version=5747&cstk=szLZezq4)


#### 4. 小结
到现在为止，我们已经搭建了一个基于spring(spring mvc)的spring security项目。可能你会很疑惑，为什么会产生这种效果。那个输入用户名和密码的页面，我们在项目中也没有创建，是怎么出来的呢？

其实这一切都是经过我们上述的配置，我们创建并注册了spring security的过滤器。是这些过滤器为我们做到的。除此之外，spring security还为我们做了额外的其他的保护。总的来说，经过我们上述的配置后，spring security为我们的应用提供了以下默认功能：
1. 访问应用中的每个URL都需要进行验证
2. 生成一个登陆表单
3. 允许用户使用username和password来登陆
4. 允许用户注销
5. CSRF攻击拦截
6. Session Fixation（session固定攻击）
7. 安全Header集成  
    7.1 HTTP Strict Transport Security for secure requests  
    7.2 X-Content-Type-Options integration  
    7.3 缓存控制 (can be overridden later by your application to allow caching of your static resources)  
    7.4 X-XSS-Protection integration  
    7.5 X-Frame-Options integration to help prevent Clickjacking  
8. Integrate with the following Servlet API methods  
    8.1 HttpServletRequest#getRemoteUser()  
    8.2 HttpServletRequest.html#getUserPrincipal()  
    8.3 HttpServletRequest.html#isUserInRole(java.lang.String)  
    8.4 HttpServletRequest.html#login(java.lang.String, java.lang.String)  
    8.5 HttpServletRequest.html#logout()  

下一节，通过spring security过滤器的创建和注册源码的分析，你将会了解这一切！

## 四、spring security过滤器的创建与注册原理

#### 1. Spring Security过滤器的创建原理
让我们首先看下MySecurityConfig类
```java
@EnableWebSecurity
@Configuration
public class MySecurityConfig extends WebSecurityConfigurerAdapter {
    
    @Autowired
    public void configUser(AuthenticationManagerBuilder builder) throws Exception {
        builder
            .inMemoryAuthentication()
                //创建用户名为user，密码为password的用户
                .withUser("user").password("password").roles("USER");
    }
}
```
可以看到MySecurityConfig上的@EnableWebSecurity注解，查看该注解的源码
```java
@Retention(value = java.lang.annotation.RetentionPolicy.RUNTIME)
@Target(value = { java.lang.annotation.ElementType.TYPE })
@Documented
@Import({ WebSecurityConfiguration.class,
        SpringWebMvcImportSelector.class })
@EnableGlobalAuthentication
@Configuration
public @interface EnableWebSecurity {

    /**
     * Controls debugging support for Spring Security. Default is false.
     * @return if true, enables debug support with Spring Security
     */
    boolean debug() default false;
}
```
@EnableWebSecurity上的@Import注解引入了两个类WebSecurityConfiguration和SpringWebMvcImportSelector，spring security的过滤器正是由WebSecurityConfiguration创建。让我们看下WebSecurityConfiguration的部分源码
```java
...
    //查看AbstractSecurityWebApplicationInitializer的源码可以看到
    //AbstractSecurityWebApplicationInitializer.DEFAULT_FILTER_NAME = "springSecurityFilterChain"
    @Bean(name = AbstractSecurityWebApplicationInitializer.DEFAULT_FILTER_NAME)
    public Filter springSecurityFilterChain() throws Exception {
        boolean hasConfigurers = webSecurityConfigurers != null
                && !webSecurityConfigurers.isEmpty();
        //如果没有配置类那么就new一个WebSecurityConfigurerAdapter,也就是说我们没有配置MySecurityConfig或者说其没有被spring扫描到
        if (!hasConfigurers) {
            WebSecurityConfigurerAdapter adapter = objectObjectPostProcessor
                    .postProcess(new WebSecurityConfigurerAdapter() {
                    });
            webSecurity.apply(adapter);
        }
        //创建Filter
        return webSecurity.build();
    }
...
```
从源码中可以看到通过WebSecurity.build()创建出名字为springSecurityFilterChain的Filter对象。（特别说明一下，一定要保证我们的MySecurityConfig类注解了@Configuration并可以被spring扫描到，如果没有被sping扫描到，那么spring security会认为没有配置类，就会新new 出一个WebSecurityConfigureAdapter对象，这会导致我们配置的用户名和密码失效。）那么该Filter的类型是什么呢？别着急，我们先来看下WeSecurity的继承体系。

![WeSecurity的继承体系](https://note.youdao.com/yws/api/personal/file/965F9F015CED49ED9A230290E48E7C48?method=getImage&version=5961&cstk=szLZezq4)

build方法定义在AbstractSecurityBuilder中，源码如下：
```java
...
public final O build() throws Exception {
        if (this.building.compareAndSet(false, true)) {
            //通过doBuild方法创建
            this.object = doBuild();
            return this.object;
        }
        throw new AlreadyBuiltException("This object has already been built");
}
...
```
doBuild方法定义在AbstractConfiguredSecurityBuilder中，源码如下：
```java
...
protected final O doBuild() throws Exception {
        synchronized (configurers) {
            buildState = BuildState.INITIALIZING;

            beforeInit();
            init();

            buildState = BuildState.CONFIGURING;

            beforeConfigure();
            configure();

            buildState = BuildState.BUILDING;

            //performBuild方法创建
            O result = performBuild();

            buildState = BuildState.BUILT;

            return result;
        }
    }
...
```
performBuild()方法定义在WebSecurity中，源码如下
```java
...
protected Filter performBuild() throws Exception {
    Assert.state(
            !securityFilterChainBuilders.isEmpty(),
            "At least one SecurityBuilder<? extends SecurityFilterChain> needs to be specified. Typically this done by adding a @Configuration that extends WebSecurityConfigurerAdapter. More advanced users can invoke "
                    + WebSecurity.class.getSimpleName()
                    + ".addSecurityFilterChainBuilder directly");
    int chainSize = ignoredRequests.size() + securityFilterChainBuilders.size();
    List<SecurityFilterChain> securityFilterChains = new ArrayList<SecurityFilterChain>(
            chainSize);
    for (RequestMatcher ignoredRequest : ignoredRequests) {
        securityFilterChains.add(new DefaultSecurityFilterChain(ignoredRequest));
    }
    for (SecurityBuilder<? extends SecurityFilterChain> securityFilterChainBuilder : securityFilterChainBuilders) {
        securityFilterChains.add(securityFilterChainBuilder.build());
    }

    //创建FilterChainProxy
    FilterChainProxy filterChainProxy = new FilterChainProxy(securityFilterChains);
    if (httpFirewall != null) {
        filterChainProxy.setFirewall(httpFirewall);
    }
    filterChainProxy.afterPropertiesSet();

    Filter result = filterChainProxy;
    if (debugEnabled) {
        logger.warn("\n\n"
                + "********************************************************************\n"
                + "**********        Security debugging is enabled.       *************\n"
                + "**********    This may include sensitive information.  *************\n"
                + "**********      Do not use in a production system!     *************\n"
                + "********************************************************************\n\n");
        result = new DebugFilter(filterChainProxy);
    }
    postBuildAction.run();
    return result;
}
...
```
不关心其具体实现，我们从源码中看到spring security创建的过滤器类型为FilterChainProxy。由此完成过滤器的创建。

#### 2. Spring Security过滤器的注册原理
看下我们创建的SecurityInitializer类：
```java
public class SecurityInitializer extends AbstractSecurityWebApplicationInitializer {

}
```
这段代码虽然很简单，但却是注册过滤器所必须的。

根据Servlet3.0中，提供了ServletContainerInitializer接口，该接口提供了一个onStartup方法，用于在容器启动时动态注册Servlet,Filter,Listener等。因为我们建立的是web项目，那我们的依赖中肯定是由spring-web依赖的

![ServletContainerInitializer](https://note.youdao.com/yws/api/personal/file/2B4C6161418B43D982F07F70858FE880?method=getImage&version=5962&cstk=szLZezq4)

根据Servlet 3.0规范，Servlet容器在启动时，会负责创建图中红色箭头所指的类，即SpringServletContainerInitializer，该类是ServletContainerInitializer的实现类。那么该类必有onStartup方法。让我们看下它的源码

```java
package org.springframework.web;

import java.lang.reflect.Modifier;
import java.util.LinkedList;
import java.util.List;
import java.util.ServiceLoader;
import java.util.Set;
import javax.servlet.ServletContainerInitializer;
import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.annotation.HandlesTypes;

import org.springframework.core.annotation.AnnotationAwareOrderComparator;

@HandlesTypes(WebApplicationInitializer.class)
public class SpringServletContainerInitializer implements ServletContainerInitializer {
    @Override
    public void onStartup(Set<Class<?>> webAppInitializerClasses, ServletContext servletContext)
            throws ServletException {

        List<WebApplicationInitializer> initializers = new LinkedList<WebApplicationInitializer>();

        if (webAppInitializerClasses != null) {
            for (Class<?> waiClass : webAppInitializerClasses) {
                //如果waiClass不为接口，抽象类，并且属于WebApplicationInitializer类型
                //那么通过反射构造该接口的实例。
                if (!waiClass.isInterface() && !Modifier.isAbstract(waiClass.getModifiers()) &&
                        WebApplicationInitializer.class.isAssignableFrom(waiClass)) {
                    try {
                        initializers.add((WebApplicationInitializer) waiClass.newInstance());
                    }
                    catch (Throwable ex) {
                        throw new ServletException("Failed to instantiate WebApplicationInitializer class", ex);
                    }
                }
            }
        }

        if (initializers.isEmpty()) {
            servletContext.log("No Spring WebApplicationInitializer types detected on classpath");
            return;
        }

        AnnotationAwareOrderComparator.sort(initializers);
        servletContext.log("Spring WebApplicationInitializers detected on classpath: " + initializers);

        for (WebApplicationInitializer initializer : initializers) {
            //调用所有WebApplicationInitializer实例的onStartup方法
            initializer.onStartup(servletContext);
        }
    }

}
```
请注意该类上的@HandlesTypes(WebApplicationInitializer.class)注解，根据Sevlet3.0规范，Servlet容器要负责以Set集合的方式注入指定类的子类（包括接口，抽象类）。其中AbstractSecurityWebApplicationInitializer是WebApplicationInitializer的抽象子类，我我们看下它的onStartup方法

```java
...
public final void onStartup(ServletContext servletContext) throws ServletException {
        beforeSpringSecurityFilterChain(servletContext);
        if (this.configurationClasses != null) {
            AnnotationConfigWebApplicationContext rootAppContext = new AnnotationConfigWebApplicationContext();
            rootAppContext.register(this.configurationClasses);
            servletContext.addListener(new ContextLoaderListener(rootAppContext));
        }
        if (enableHttpSessionEventPublisher()) {
            servletContext.addListener(
                    "org.springframework.security.web.session.HttpSessionEventPublisher");
        }
        servletContext.setSessionTrackingModes(getSessionTrackingModes());
        //注册过滤器
        insertSpringSecurityFilterChain(servletContext);
        afterSpringSecurityFilterChain(servletContext);
}
...
```
该类中的insertSpringSecurityFilterChain(servletContext)就是在注册过滤器。因为在过滤器创建中所说的springSecurityFilterChain，它其实是spring中的bean，而servletContext也必定可以获取到该bean。我们接着看insertSpringSecurityFilterChain的源码
```java
...
public static final String DEFAULT_FILTER_NAME = "springSecurityFilterChain";

private void insertSpringSecurityFilterChain(ServletContext servletContext) {

    String filterName = DEFAULT_FILTER_NAME;
    //通过DelegatingFilterProxy代理
    DelegatingFilterProxy springSecurityFilterChain = new DelegatingFilterProxy(
            filterName);
    String contextAttribute = getWebApplicationContextAttribute();
    if (contextAttribute != null) {
        springSecurityFilterChain.setContextAttribute(contextAttribute);
    }
    //完成过滤器的注册
    registerFilter(servletContext, true, filterName, springSecurityFilterChain);
}
...
```
一开始我们就提到了调用过滤器链springSecurityFilterChain需要DelegatingFilterProxy进行代理，将其与web.xml联系起来。这段代码就是很好的证明。DelegatingFilterProxy中维护了一个类型为String，名字叫做targetBeanName的字段，targetBeanName就是DelegatingFilterProxy所代理的类的名称。最后通过registerFilter最终完成过滤器的注册。

## 五、spring security 认证和授权原理

在上一节我们讨论了spring security过滤器的创建和注册原理。请记住springSecurityFilterChain（类型为FilterChainProxy）是实际起作用的过滤器链，DelegatingFilterProxy起到代理作用。

但是这还没有解决我们最初的所有问题，那就是虽然创建了springSecurityFilterChain过滤器链，那么过滤器链中的过滤器是如何一一创建的？这些过滤器是如何实现认证和授权的？本节我们来讨论这个问题。

注意：本节代码示例，采用的依然第二节中基于Java配置的搭建中的代码为例。

#### 1. 过滤器的创建
我们创建的MySecurityConfig继承了WebSecurityConfigurerAdapter。WebSecurityConfigurerAdapter中有个configure(HttpSecurity http)的方法：
```java
protected void configure(HttpSecurity http) throws Exception {
        http
            .authorizeRequests() //拦截请求，创建FilterSecurityInterceptor
                .anyRequest().authenticated() //在创建过滤器的基础上的一些自定义配置
                .and() //用and来表示配置过滤器结束，以便进行下一个过滤器的创建和配置
            .formLogin().and() //设置表单登录，创建UsernamePasswordAuthenticationFilter
            .httpBasic(); //basic验证，创建BasicAuthenticationFilter
}
```
该方法用来实现spring security的一些自定义的配置，其中就包括Filter的创建。其中http.authorizeRequests()、http.formLogin()、http.httpBasic()分别创建了ExpressionUrlAuthorizationConfigurer，FormLoginConfigurer，HttpBasicConfigurer。在三个类从父级一直往上找，会发现它们都是SecurityConfigurer的子类。SecurityConfigurer中又有configure方法。该方法被子类实现就用于创建各个过滤器，并将过滤器添加进HttpSecurity中维护的装有Filter的List中，比如HttpBasicConfigurer中的configure方法，源码如下：
```java
public void configure(B http) throws Exception {
        AuthenticationManager authenticationManager = http
                .getSharedObject(AuthenticationManager.class);
        //创建BasicAuthenticationFilter过滤器
        BasicAuthenticationFilter basicAuthenticationFilter = new BasicAuthenticationFilter(
                authenticationManager, this.authenticationEntryPoint);
        if (this.authenticationDetailsSource != null) {
            basicAuthenticationFilter
                    .setAuthenticationDetailsSource(this.authenticationDetailsSource);
        }
        RememberMeServices rememberMeServices = http.getSharedObject(RememberMeServices.class);
        if(rememberMeServices != null) {
            basicAuthenticationFilter.setRememberMeServices(rememberMeServices);
        }
        basicAuthenticationFilter = postProcess(basicAuthenticationFilter);
        //添加过滤器
        http.addFilter(basicAuthenticationFilter);
}
```
另外，并非所有的过滤器都是在configure中进行创建的，比如UsernamePasswordAuthenticationFilter是在调用FormLoginConfigurer的构造方法时创建的。FormLoginConfigurer部分源码如下：
```java
public FormLoginConfigurer() {
        super(new UsernamePasswordAuthenticationFilter(), null);
        usernameParameter("username");
        passwordParameter("password");
}
```
HttpSecurity的父类是AbstractConfiguredSecurityBuilder，该类中有个configure方法用来获取所有SecurityConfigurer，并调用所有SecurityConfigurer的configure方法。源码如下：
```java
private void configure() throws Exception {
        //获取所有SecurityConfigurer类
        Collection<SecurityConfigurer<O, B>> configurers = getConfigurers();

        for (SecurityConfigurer<O, B> configurer : configurers) {
            //调用所有SecurityConfigurer的configure方法
            configurer.configure((B) this);
        }
}
```
以上就是过滤器的创建过程。当我们的MySecurityConfig继承了WebSecurityConfigurerAdapter以后，就默认有了configure(HttpSecurity http)方法。我们也可以在MySecurityConfig中重写此方法来进行更灵活的配置。
```java
@Override
    protected void configure(HttpSecurity http) throws Exception {
        http
        .authorizeRequests() //注册FilterSecurityInterceptor
             .antMatchers("/index.html").permitAll()//访问index.html不要权限验证
             .anyRequest().authenticated()//其他所有路径都需要权限校验
        .and()
             .csrf().disable()//默认开启，可以显示关闭
        .formLogin()  //内部注册 UsernamePasswordAuthenticationFilter
            .loginPage("/login.html") //表单登录页面地址
            .loginProcessingUrl("/login")//form表单POST请求url提交地址，默认为/login
            .passwordParameter("password")//form表单用户名参数名
            .usernameParameter("username") //form表单密码参数名
            .successForwardUrl("/success.html")  //登录成功跳转地址
            .failureForwardUrl("/error.html") //登录失败跳转地址
            //.defaultSuccessUrl()//如果用户没有访问受保护的页面，默认跳转到页面
            //.failureUrl()
            //.failureHandler(AuthenticationFailureHandler)
            //.successHandler(AuthenticationSuccessHandler)
            //.failureUrl("/login?error")
            .permitAll();//允许所有用户都有权限访问loginPage，loginProcessingUrl，failureForwardUrl
    }
```
虽然我们上面仅仅看到了三种过滤器的创建，但是真正创建的远不止三种，spring secuirty会默认帮我们注册一些过滤器。比如SecurityContextPersistenceFilter，该过滤器用于在我们请求到来时，将SecurityContext从Session中取出放入SecuirtyContextHolder中供我们使用。并在请求结束时将SecuirtyContext存进Session中便于下次使用。还有DefaultLoginPageGeneratingFilter，该过滤器在我们没有自定义配置loginPage时会自动生成，用于生成我们默认的登录页面，也就是我们一开始在搭建中看到的登录页面。对于自定义配置spring security详细参考javaDoc。spring secuirty核心过滤器以及其顺序如下（并未包括所有）：

![spring secuirty核心过滤器以及其顺序](https://note.youdao.com/yws/api/personal/file/D8B7253A683B4EBD90D352719615FEF1?method=getImage&version=5960&cstk=szLZezq4)

#### 2. 认证与授权
　认证(Authentication)：确定一个用户的身份的过程。授权(Authorization)：判断一个用户是否有访问某个安全对象的权限。下面讨论一下spring security中最基本的认证与授权。

首先明确一下在认证与授权中关键的三个过滤器，其他过滤器不讨论：

    1. UsernamePasswordAuthenticationFilter：该过滤器用于拦截我们表单提交的请求（默认为/login），进行用户的认证过程吧。
    
    2. ExceptionTranslationFilter：该过滤器主要用来捕获处理spring security抛出的异常，异常主要来源于FilterSecurityInterceptor。
    
    3. FilterSecurityInterceptor：该过滤器主要用来进行授权判断。

下面根据我们访问应用的顺序并结合源码分析一下spring security的认证与授权。代码仍然是前面基于Java配置的搭建中的

1. 我们在浏览器中输入http://localhost:9090/ 访问应用，因为我们的路径被spring secuirty保护起来了，我们是没有权限访问的，所以我们会被引导至登录页面进行登录。

![登陆界面](https://note.youdao.com/yws/api/personal/file/4C189F378ED642D29B1CFEB7E0710953?method=getImage&version=5821&cstk=szLZezq4)

此路径因为不是表单提交的路径(/login)，该过程主要起作用的过滤器为FilterSecurityInterceptor。其部分源码如下：
```java
...
    public void doFilter(ServletRequest request, ServletResponse response,
            FilterChain chain) throws IOException, ServletException {
        FilterInvocation fi = new FilterInvocation(request, response, chain);
        invoke(fi);
    }
    public void invoke(FilterInvocation fi) throws IOException, ServletException {
        //过滤器对每个请求只处理一次
        if ((fi.getRequest() != null)
                && (fi.getRequest().getAttribute(FILTER_APPLIED) != null)
                && observeOncePerRequest) {
            // filter already applied to this request and user wants us to observe
            // once-per-request handling, so don't re-do security checking
            fi.getChain().doFilter(fi.getRequest(), fi.getResponse());
        }
        else {
            // first time this request being called, so perform security checking
            if (fi.getRequest() != null) {
                fi.getRequest().setAttribute(FILTER_APPLIED, Boolean.TRUE);
            }

            //前处理
            InterceptorStatusToken token = super.beforeInvocation(fi);

            try {
                fi.getChain().doFilter(fi.getRequest(), fi.getResponse());
            }
            finally {
                //使SecurityContextHolder中的Authentication保持原样，因为RunAsManager会暂时改变
                //其中的Authentication
                super.finallyInvocation(token);
            }

            //调用后的处理
            super.afterInvocation(token, null);
        }
    }
...
```
真正进行权限判断的为beforeInvocation，该方法定义在FilterSecurityInterceptor的父类AbstractSecurityInterceptor中，源码如下：
```java
...
    protected InterceptorStatusToken beforeInvocation(Object object) {
        Assert.notNull(object, "Object was null");
        final boolean debug = logger.isDebugEnabled();

        //判断object是否为过滤器支持的类型，在这里是FilterInvocation(里面记录包含了请求的request,response,FilterChain)
        //这里可以把FilterInvocation看做是安全对象，因为通过它可以获得request,通过request可以获得请求的URI。
        //而实际的安全对象就是URI
        if (!getSecureObjectClass().isAssignableFrom(object.getClass())) {
            throw new IllegalArgumentException(
                    "Security invocation attempted for object "
                            + object.getClass().getName()
                            + " but AbstractSecurityInterceptor only configured to support secure objects of type: "
                            + getSecureObjectClass());
        }

        
        //获取安全对象所对应的ConfigAttribute，ConfigAtrribute实际就是访问安全所应该有的权限集。
        Collection<ConfigAttribute> attributes = this.obtainSecurityMetadataSource()
                .getAttributes(object);

        //判断安全对象是否拥有权限集，没有的话说明所访问的安全对象是一个公共对象，就是任何人都可以访问的。
        if (attributes == null || attributes.isEmpty()) {
            //如果rejectPublicInvocations为true,说明不支持公共对象的访问，此时会抛出异常。
            if (rejectPublicInvocations) {
                throw new IllegalArgumentException(
                        "Secure object invocation "
                                + object
                                + " was denied as public invocations are not allowed via this interceptor. "
                                + "This indicates a configuration error because the "
                                + "rejectPublicInvocations property is set to 'true'");
            }

            if (debug) {
                logger.debug("Public object - authentication not attempted");
            }

            publishEvent(new PublicInvocationEvent(object));

            return null; // no further work post-invocation
        }

        if (debug) {
            logger.debug("Secure object: " + object + "; Attributes: " + attributes);
        }

        //判断SecurityCntext中是否存在Authentication,不存在则说明访问着根本没登录
        //调用下面的credentialsNotFound()方法则会抛出一个AuthenticationException，
        //该异常会被ExceptionTranslationFilter捕获，并做出处理。
        //不过默认情况下Authentication不会为null,因为AnonymouseFilter会默认注册到
        //过滤链中，如果用户没登录的话，会将其当做匿名用户(Anonymouse User)来对待。
        //除非你自己将AnonymouseFilter从过滤链中去掉。
        if (SecurityContextHolder.getContext().getAuthentication() == null) {
            credentialsNotFound(messages.getMessage(
                    "AbstractSecurityInterceptor.authenticationNotFound",
                    "An Authentication object was not found in the SecurityContext"),
                    object, attributes);
        }

        //Autentication存在，则说明用户已经被认证（但是不表示已登录，因为匿名用户也是相当于被认证的），
        //判断用户是否需要再次被认证，如果你配置了每次访问必须重新验证，那么就会再次调用AuthenticationManager
        //的authenticate方法进行验证。
        Authentication authenticated = authenticateIfRequired();

        // Attempt authorization
        try {
            //判断用户是否有访问被保护对象的权限。
            //ed。默认的AccessDesicisonManager的实现类是AffirmativeBased
            //AffirmativeBased采取投票的形式判断用户是否有访问安全对象的权限
            //票就是配置的Role。AffirmativeBased采用WebExpressionVoter进行投票
            this.accessDecisionManager.decide(authenticated, object, attributes);
        }
        catch (AccessDeniedException accessDeniedException) {
            publishEvent(new AuthorizationFailureEvent(object, attributes, authenticated,
                    accessDeniedException));

            throw accessDeniedException;
        }

        if (debug) {
            logger.debug("Authorization successful");
        }

        if (publishAuthorizationSuccess) {
            publishEvent(new AuthorizedEvent(object, attributes, authenticated));
        }

        // Attempt to run as a different user
        Authentication runAs = this.runAsManager.buildRunAs(authenticated, object,
                attributes);

        if (runAs == null) {
            if (debug) {
                logger.debug("RunAsManager did not change Authentication object");
            }

            // no further work post-invocation
            return new InterceptorStatusToken(SecurityContextHolder.getContext(), false,
                    attributes, object);
        }
        else {
            if (debug) {
                logger.debug("Switching to RunAs Authentication: " + runAs);
            }

            SecurityContext origCtx = SecurityContextHolder.getContext();
            SecurityContextHolder.setContext(SecurityContextHolder.createEmptyContext());
            SecurityContextHolder.getContext().setAuthentication(runAs);

            // need to revert to token.Authenticated post-invocation
            return new InterceptorStatusToken(origCtx, true, attributes, object);
        }
    }
...
```
看这段代码，请明确几点:

- beforeInvocation(Object object)中的object为安全对象，类型为FilterInvocation。安全对象就是受spring security保护的对象。虽然按道理来说安全对象应该是我们访问的url，但是FilterInvocation中封装了request，那么url也可以获取到。

- Collection<ConfigAttribute> attributes = this.obtainSecurityMetadataSource().getAttributes(object) 每个安全对象都会有对应的访问权限集(Collection<ConfigAttribute>)，而且在容器启动后所有安全对象的所有权限集就已经被获取到并被放在安全元数据中（SecurityMetadataSource中），通过安全元数据可以获取到各个安全对象的权限集。因为我们每个安全对象都是登录才可以访问的（anyRequest().authenticated()），这里我们只需要知道此时每个对象的权限集只有一个元素，并且是authenticated。如果一个对象没有权限集，说明它是一个公共对象，不受spring security保护。

- 当我们没有登录时，我们会被当做匿名用户（Anonymouse）来看待。被当做匿名用户对待是AnonymouseAuthenticationFilter来拦截封装成一个Authentication对象，当用户被认证后就会被封装成一个Authentication对象。Authentication对象中封装了用户基本信息，该对象会在认证中做详细介绍。AnonymouseAuthenticationFilter也是默认被注册的。

- 最中进行授权判断的是AccessDecisionManager的子类AffirmativeBased的decide方法。我在来看其decide的源码：
```java
...
public void decide(Authentication authentication, Object object,
            Collection<ConfigAttribute> configAttributes) throws AccessDeniedException {
        int deny = 0;

        for (AccessDecisionVoter voter : getDecisionVoters()) {
            //根据用户的authenticton和权限集得出能否访问的结果
            int result = voter.vote(authentication, object, configAttributes);

            if (logger.isDebugEnabled()) {
                logger.debug("Voter: " + voter + ", returned: " + result);
            }

            switch (result) {
            case AccessDecisionVoter.ACCESS_GRANTED:
                return;
            case AccessDecisionVoter.ACCESS_DENIED:
                deny++;

                break;

            default:
                break;
            }
        }

        if (deny > 0) {
            //如果deny>0说明没有足够的权限去访问安全对象，此时抛出的
            //AccessDeniedException会被ExceptionTranslationFilter捕获处理。
            throw new AccessDeniedException(messages.getMessage(
                    "AbstractAccessDecisionManager.accessDenied", "Access is denied"));
        }

        // To get this far, every AccessDecisionVoter abstained
        checkAllowIfAllAbstainDecisions();
}
...
```
因为我们首次登录，所以会抛出AccessDeniedexception。此异常会被ExceptionTranslationFilter捕获并进行处理的。其部分源码如下：
```java
...
public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) req;
        HttpServletResponse response = (HttpServletResponse) res;

        try {
            chain.doFilter(request, response);

            logger.debug("Chain processed normally");
        }
        catch (IOException ex) {
            throw ex;
        }
        catch (Exception ex) {
            // Try to extract a SpringSecurityException from the stacktrace
            Throwable[] causeChain = throwableAnalyzer.determineCauseChain(ex);
            RuntimeException ase = (AuthenticationException) throwableAnalyzer
                    .getFirstThrowableOfType(AuthenticationException.class, causeChain);

            if (ase == null) {
                ase = (AccessDeniedException) throwableAnalyzer.getFirstThrowableOfType(
                        AccessDeniedException.class, causeChain);
            }

            if (ase != null) {
                //真正处理异常的地方
                handleSpringSecurityException(request, response, chain, ase);
            }
            else {
                // Rethrow ServletExceptions and RuntimeExceptions as-is
                if (ex instanceof ServletException) {
                    throw (ServletException) ex;
                }
                else if (ex instanceof RuntimeException) {
                    throw (RuntimeException) ex;
                }

                // Wrap other Exceptions. This shouldn't actually happen
                // as we've already covered all the possibilities for doFilter
                throw new RuntimeException(ex);
            }
        }
}

private void handleSpringSecurityException(HttpServletRequest request,
            HttpServletResponse response, FilterChain chain, RuntimeException exception)
            throws IOException, ServletException {
        if (exception instanceof AuthenticationException) {
            logger.debug(
                    "Authentication exception occurred; redirecting to authentication entry point",
                    exception);
            //未被认证，引导去登录
            sendStartAuthentication(request, response, chain,
                    (AuthenticationException) exception);
        }
        else if (exception instanceof AccessDeniedException) {
            Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
            if (authenticationTrustResolver.isAnonymous(authentication) || authenticationTrustResolver.isRememberMe(authentication)) {
                logger.debug(
                        "Access is denied (user is " + (authenticationTrustResolver.isAnonymous(authentication) ? "anonymous" : "not fully authenticated") + "); redirecting to authentication entry point",
                        exception);
                //如果为匿名用户说明未登录，引导去登录
                sendStartAuthentication(
                        request,
                        response,
                        chain,
                        new InsufficientAuthenticationException(
                                "Full authentication is required to access this resource"));
            }
            else {
                logger.debug(
                        "Access is denied (user is not anonymous); delegating to AccessDeniedHandler",
                        exception);
                //用户已登录，但是没有足够权限去访问安全对象，说明权限不足。进行
                //权限不足的提醒
                accessDeniedHandler.handle(request, response,
                        (AccessDeniedException) exception);
            }
        }
}
...
```
因为我们是以匿名用户的身份进行登录的，所以，会被引导去登录页面。登录页面的创建是由默认注册的过滤器DefaultLoginPageGeneratingFilter产生的。具体怎么产生的这里不做分析。我们只需要是谁做的就可以了。实际在使用时我们也不大可能去用默认生成的登录页面，因为太丑了。。。

<br>

2、在被引导至登录页面后，我们将输入用户名和密码，提交至应用。应用会校验用户名和密码，校验成功后，我们成功访问应用。

![登陆成功](https://note.youdao.com/yws/api/personal/file/024CBDB6050549E2AEE13B3AB7C3D507?method=getImage&version=5747&cstk=szLZezq4)

此时访问的路径为/login，这是UsernamePasswordAuthenticationFilter将拦截请求进行认证。UsernamePasswordAuthenticationFilter的doFilter方法定义在其父类AbstractAuthenticationProcessingFilter中，源码如下：
```java
public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest request = (HttpServletRequest) req;
        HttpServletResponse response = (HttpServletResponse) res;

        //判断请求是否需要进行验证处理。默认对/login并且是POST请求的路径进行拦截
        if (!requiresAuthentication(request, response)) {
            chain.doFilter(request, response);

            return;
        }

        if (logger.isDebugEnabled()) {
            logger.debug("Request is to process authentication");
        }

        Authentication authResult;

        try {
            //调用UsernamePasswordAuthenticationFilter的attemptAuthentication方法进行验证，并返回
            //完整的被填充的Authentication对象
            authResult = attemptAuthentication(request, response);
            if (authResult == null) {
                // return immediately as subclass has indicated that it hasn't completed
                // authentication
                return;
            }

            //进行session固定攻击的处理
            sessionStrategy.onAuthentication(authResult, request, response);
        }
        catch (InternalAuthenticationServiceException failed) {
            logger.error(
                    "An internal error occurred while trying to authenticate the user.",
                    failed);
            unsuccessfulAuthentication(request, response, failed);

            return;
        }
        catch (AuthenticationException failed) {
            // 认证失败后的处理
            unsuccessfulAuthentication(request, response, failed);

            return;
        }

        // Authentication success
        if (continueChainBeforeSuccessfulAuthentication) {
            chain.doFilter(request, response);
        }

        //认证成功后的处理
        successfulAuthentication(request, response, chain, authResult);
  }
```
实际认证发生在UsernamePasswordAuthenticationFilter的attemptAuthentication中，如果认证失败，则会调用unsuccessfulAuthentication进行失败后的处理，一般是提示用户认证失败，要求重新输入用户名和密码，如果认证成功，那么会调用successfulAuthentication进行成功后的处理，一般是将Authentication存进SecurityContext中并跳转至之前访问的页面或者默认页面（这部分在读者读完本节后自行去看源码是怎么处理的，这里不做讨论，现在只需知道会跳到一开始我们访问的页面中）。下面我们来看认证即attemptAuthentication的源码：
```java
...
public Authentication attemptAuthentication(HttpServletRequest request,
            HttpServletResponse response) throws AuthenticationException {
        if (postOnly && !request.getMethod().equals("POST")) {
            throw new AuthenticationServiceException(
                    "Authentication method not supported: " + request.getMethod());
        }

        String username = obtainUsername(request);
        String password = obtainPassword(request);

        if (username == null) {
            username = "";
        }

        if (password == null) {
            password = "";
        }

        username = username.trim();

        //将用户名和密码封装在Authentication的实现UsernamePasswordAuthenticationToken
        //以便于AuthentictionManager进行认证
        UsernamePasswordAuthenticationToken authRequest = new UsernamePasswordAuthenticationToken(
                username, password);

        // Allow subclasses to set the "details" property
        setDetails(request, authRequest);

        //获得AuthenticationManager进行认证
        return this.getAuthenticationManager().authenticate(authRequest);
}
...
```
spring security在进行认证时，会将用户名和密码封装成一个Authentication对象，在进行认证后，会将Authentication的权限等信息填充完全返回。Authentication会被存在SecurityContext中，供应用之后的授权等操作使用。此处介绍下Authentication，Authentication存储的就是访问应用的用户的一些信息。下面是Authentication源码：
```java
public interface Authentication extends Principal, Serializable {
    //用户的权限集合
    Collection<? extends GrantedAuthority> getAuthorities();

    //用户登录的凭证，一般指的就是密码
    Object getCredentials();

    //用户的一些额外的详细信息，一般不用
    Object getDetails();

    //这里认为Principal就为登录的用户
    Object getPrincipal();

    //是否已经被认证了
    boolean isAuthenticated();

    //设置认证的状态
    void setAuthenticated(boolean isAuthenticated) throws IllegalArgumentException;
}
```
讲解了Authentication后，我们回过头来再看attemptAuthentication方法，该方法会调用AuthenticationManager的authenticate方法进行认证并返回一个填充完整的Authentication对象。

在这里我们又要讲解一下认证的几个核心的类，很重要！

a). AuthenticationManager　　b).ProviderManager　　c).AuthenticationProvider　　d).UserDetailsService　　e).UserDetails

现在来说一下这几个类的作用以及关联关系。

a). AuthenticationManager是一个接口，提供了authenticate方法用于认证。

b). AuthenticationManager有一个默认的实现ProviderManager，其实现了authenticate方法。

c). ProviderManager内部维护了一个存有AuthenticationProvider的集合，ProviderManager实现的authenticate方法再调用这些AuthenticationProvider的authenticate方法去认证，表单提交默认用的AuthenticationProvider实现是DaoAuthenticationProvider。

d). AuthenticationProvider中维护了UserDetailsService，我们使用内存中的用户，默认的实现是InMemoryUserDetailsManager。UserDetailsService用来查询用户的详细信息，该详细信息就是UserDetails。UserDetails的默认实现是User。查询出来UserDetails后再对用户输入的密码进行校验。校验成功则将UserDetails中的信息填充进Authentication中返回。校验失败则提醒用户密码错误。

以上说的这些接口的实现类是由我们在MySecurityConfig中配置时生成的，即下面的代码:
```java
@Autowired
    public void configUser(AuthenticationManagerBuilder builder) throws Exception {
        builder
            .inMemoryAuthentication()
                //创建用户名为user，密码为password的用户
                .withUser("user").password("password").roles("USER");
    }
```
这里不再讨论具体是怎么生成的，记住即可。因为我们实际在项目中一般都会用自定义的这些核心认证类。

下面我们来分析源码，先来看ProviderManager的authenticate方法：
```java
...
public Authentication authenticate(Authentication authentication)
            throws AuthenticationException {
        Class<? extends Authentication> toTest = authentication.getClass();
        AuthenticationException lastException = null;
        Authentication result = null;
        boolean debug = logger.isDebugEnabled();

        //获取所有AuthenticationProvider，循环进行认证
        for (AuthenticationProvider provider : getProviders()) {
            if (!provider.supports(toTest)) {
                continue;
            }

            if (debug) {
                logger.debug("Authentication attempt using "
                        + provider.getClass().getName());
            }

            try {
                //对authentication进行认证
                result = provider.authenticate(authentication);

                if (result != null) {
                    //填充成完整的Authentication
                    copyDetails(authentication, result);
                    break;
                }
            }
            catch (AccountStatusException e) {
                prepareException(e, authentication);
                // SEC-546: Avoid polling additional providers if auth failure is due to
                // invalid account status
                throw e;
            }
            catch (InternalAuthenticationServiceException e) {
                prepareException(e, authentication);
                throw e;
            }
            catch (AuthenticationException e) {
                lastException = e;
            }
        }

        if (result == null && parent != null) {
            // Allow the parent to try.
            try {
                result = parent.authenticate(authentication);
            }
            catch (ProviderNotFoundException e) {
                // ignore as we will throw below if no other exception occurred prior to
                // calling parent and the parent
                // may throw ProviderNotFound even though a provider in the child already
                // handled the request
            }
            catch (AuthenticationException e) {
                lastException = e;
            }
        }

        if (result != null) {
            if (eraseCredentialsAfterAuthentication
                    && (result instanceof CredentialsContainer)) {
                // Authentication is complete. Remove credentials and other secret data
                // from authentication
                ((CredentialsContainer) result).eraseCredentials();
            }

            eventPublisher.publishAuthenticationSuccess(result);
            return result;
        }

        // Parent was null, or didn't authenticate (or throw an exception).

        if (lastException == null) {
            //如果所有的AuthenticationProvider进行认证完result仍然为null
            //此时表示为提供AuthenticationProvider，抛出ProviderNotFoundException异常
            lastException = new ProviderNotFoundException(messages.getMessage(
                    "ProviderManager.providerNotFound",
                    new Object[] { toTest.getName() },
                    "No AuthenticationProvider found for {0}"));
        }

        prepareException(lastException, authentication);

        throw lastException;
}
...
```
ProviderManager用AuthenticationProvider对authentication进行认证。如果没有提供AuthenticationProvider，那么最终将抛出ProviderNotFoundException。

我们表单提交认证时，AuthenticationProvider默认的实现是DaoAuthenticationProvider，DaoAuthenticationProvider的authenticate方法定义在其父类AbstractUserDetailsAuthenticationProvider中，其源码如下：
```java
...
public Authentication authenticate(Authentication authentication)
            throws AuthenticationException {
        Assert.isInstanceOf(UsernamePasswordAuthenticationToken.class, authentication,
                messages.getMessage(
                        "AbstractUserDetailsAuthenticationProvider.onlySupports",
                        "Only UsernamePasswordAuthenticationToken is supported"));

        // Determine username
        String username = (authentication.getPrincipal() == null) ? "NONE_PROVIDED"
                : authentication.getName();

        boolean cacheWasUsed = true;
        UserDetails user = this.userCache.getUserFromCache(username);

        if (user == null) {
            cacheWasUsed = false;

            try {
                //获取UserDetails，即用户详细信息
                user = retrieveUser(username,
                        (UsernamePasswordAuthenticationToken) authentication);
            }
            catch (UsernameNotFoundException notFound) {
                logger.debug("User '" + username + "' not found");

                if (hideUserNotFoundExceptions) {
                    throw new BadCredentialsException(messages.getMessage(
                            "AbstractUserDetailsAuthenticationProvider.badCredentials",
                            "Bad credentials"));
                }
                else {
                    throw notFound;
                }
            }

            Assert.notNull(user,
                    "retrieveUser returned null - a violation of the interface contract");
        }

        try {
            preAuthenticationChecks.check(user);
            //进行密码校验
            additionalAuthenticationChecks(user,
                    (UsernamePasswordAuthenticationToken) authentication);
        }
        catch (AuthenticationException exception) {
            if (cacheWasUsed) {
                // There was a problem, so try again after checking
                // we're using latest data (i.e. not from the cache)
                cacheWasUsed = false;
                user = retrieveUser(username,
                        (UsernamePasswordAuthenticationToken) authentication);
                preAuthenticationChecks.check(user);
                additionalAuthenticationChecks(user,
                        (UsernamePasswordAuthenticationToken) authentication);
            }
            else {
                //认证失败抛出认证异常
                throw exception;
            }
        }

        postAuthenticationChecks.check(user);

        if (!cacheWasUsed) {
            this.userCache.putUserInCache(user);
        }

        Object principalToReturn = user;

        if (forcePrincipalAsString) {
            principalToReturn = user.getUsername();
        }

        //认证成功，返回装有用户权限等信息的authentication对象
        return createSuccessAuthentication(principalToReturn, authentication, user);
}
...
```
retrieveUser方法定义在DaoAuthenticationProvider中，用来获取UserDetails这里不再展示源码，请读者自行去看。你会发现获取获取UserDetails正是由其中维护的UserDetailsService来完成的。获取到UserDetails后再调用其

additionalAuthenticationChecks方法进行密码的验证。如果认证失败，则抛出AuthenticationException，如果认证成功则返回装有权限等信息的Authentication对象。

<br>

3、小节
到目前为止，我们结合我们创建的项目和spring security的源码分析了web应用认证和授权的原理。内容比较多，现在理一下重点。

1. springSecurityFilterChain中各个过滤器怎么创建的只需了解即可。不要太过关注。

2. 重点记忆UsernamePasswordAuthenticationFilter，ExceptionTranslationFilter，FilterSecurityInterceptor这三个过滤器的作用及源码分析。

3. 重要记忆认证中Authentication，AuthenticationManager，ProviderManager，AuthenticationProvider，UserDetailsService，UserDetails这些类的作用及源码分析。

4. 重点记忆授权中FilterInvoction，SecurityMetadataSource，AccessDecisionManager的作用。

5. 将这些类理解的关键是建立起关联，建立起关联的方式就是跟着本节中的案例走下去，一步步看代码如何实现的。

## 六、spring security Java配置实现自定义表单认证与授权
前面三节讲解了spring security的搭建以及简单的表单认证与授权原理。本篇将实现我们自定义的表单登录与认证。

本篇不会再讲项目的搭建过程，因为跟第二节的搭建如出一辙。本篇也不会将项目中所有的代码全部给出，因为代码量有点大。项目的代码被放在了github上，请拉下来根据讲解去看代码，代码的注释写的也比较详细。github地址https://github.com/wutianqi/spring_security_extend.git。另外，因为项目中使用了mysql数据库，对于表结构和数据这里截图会很明白的给出。


#### 1. 项目结构及表结构
1.1 项目结构

![项目结构](https://note.youdao.com/yws/api/personal/file/A6099E24CA39482B93CA8EC9C865C20E?method=getImage&version=5975&cstk=szLZezq4)

![项目结构2](https://note.youdao.com/yws/api/personal/file/7A3EDE91423B417FA39C3FE1C7A01643?method=getImage&version=5974&cstk=szLZezq4)


1.2 表结构

创建名称为`spring_security`的数据库，创建三张表：user、role、user_role

用户表（user）：
| id   | user_name | password |
| ---- | --------- | -------- |
| 1    | admin     | admin    |
| 2    | test      | test     |

角色表（role）：
| id   | role_name |
| ---- | --------- |
| 1    | user      |
| 2    | admin     |

用户角色表（user_role）：
| id   | user_id | role_id |
| ---- | ------- | ------- |
| 1    | 1       | 1       |
| 2    | 2       | 2       |

#### 2. 项目功能
在讲解代码之前还是要介绍一下本项目利用spring security实现的功能，便于读者分析代码。

2.1 本项目围绕着admin.jsp，user.jsp，other.jsp展开。

- admin.jsp只有admin角色的用户才可以访问，ls拥有admin角色。

- user.jsp有user角色或admin角色都可以访问，zs拥有user角色。

- other.jsp只要用户登录就可以访问，ww什么角色都没有。为了简单起见，项目中other.jsp就代表其他任何登录后就可以访问的路径

#### 3. 代码解读
关于spring security认证与授权原理的讲解在前一篇讲的比较清楚了，这里不再详细介绍，这里只介绍一下自己认为比较重要的代码。

3.1 MySecurityConfig

spring secuirty提供了一种后处理bean方式提供一个自定义配置过滤器的口子，就是下面这段代码：

![自定义配置过滤器](https://note.youdao.com/yws/api/personal/file/99D529E5C8FB4F9FA3283DFE02F91E07?method=getImage&version=6030&cstk=szLZezq4)

这段代码对FilterSecurityInterceptor的AccessDecisionManager属性进行了自定义的配置。目的是让spring security用我们自定义的AccessDecisionManager。

3.2 MyAccessDecisionManager

在用户没有登录时，decide中的authentication参数是AnonymousAuthenticationToken，此时他会有ROLE_ANONYMOUS的角色，就是匿名角色。这是AnonymousAuthenticationFilter来做的。

这样下面这段代码就好理解了
```java
if(authorityString.contains("ROLE_ANONYMOUS")) {
            //未登录
            throw new AccessDeniedException("未登录");
}
```

3.3 MyAuthenticationProvider

我们的MyAuthenticationProvider继承了AbstractUserDetailsAuthenticationProvider，我们自定义provider的真正认证过程实际发生在AbstractUserDetailsAuthenticationProvider的authenticate中。我们的MyAuthenticationProvider只是实现了retrieveUser来获取用户信息并在其中检查用户名是否存在，以及实现了additionalAuthenticationChecks检验用户输入的密码。其他一些诸如填充完整的Authentication的行为交给父类来做了。因为父类处理的很好所以我们无须自己再做。MySuccessHandler也是将认证成功后的处理都交给父类去处理了。

#### 4. 小节
本spring security系列，只是对我们web应用中常见的表单认证与登录进行了讲解。spring security还有很多安全功能。比如方法安全，域安全等。本文没有进行讲解。想了解更多，可以查看官方文档。自己以后也会再学，到时候也会再写相关博文。

项目地址 https://github.com/wutianqi/spring_security_extend.git