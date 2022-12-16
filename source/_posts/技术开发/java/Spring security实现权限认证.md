---
title: Spring security实现权限认证
date: 2022-12-15 23:12:12
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - Spring security实现权限认证
---
配置适配器 WebSecurityConfigurerAdapter

```java
/**
 *  spring security 核心配置文件
 */
@Configuration
public class BrowerSecurityConfig extends WebSecurityConfigurerAdapter {
    @Autowired
    private AuthenticationManager authenticationManager;
    @Autowired  //自定义的安全元   数据源     实现FilterInvocationSecurityMetadataSource
    private MyInvocationSecurityMetadataSourceService myInvocationSecurityMetadataSourceService;
    @Autowired //自定义访问决策器
    private MyAccessDecisionManager myAccessDecisionManager;

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        /**
         *  from表单登录设置
         */
        http.formLogin()
                .loginPage("")                      //登录页面                      /login
                .passwordParameter("")              //设置form表单中对应的name参数  默认为 password   下同
                .usernameParameter("")              //
                .defaultSuccessUrl("")            //认证成功后的跳转页面 默认跳转页面   可以设置是否总是默认  不是的话可以跳转与用户的target-url
                .failureUrl("")
                .failureForwardUrl("")            //登录失败 转发 的url
                .successForwardUrl("")              //登录成功 转发 的url  与successHandler对应  即处理完后请求转发的url
                .failureHandler(null)               //自定义的认证失败 做什么处理
                .successHandler(null)               //自定义认证成功 后做的处理    ----- 例如 想记录用户信息判断用户状态等
                .permitAll()                      //对于需要所有用户都可以访问的界面 或者url进行设置
                .loginProcessingUrl("")             //自定义处理认证的url    默认为    /login
                .authenticationDetailsSource(null)  //自定义身份验证的数据源  理解为查出数据库中的密码 和权限（可以不加） 然后再交给security
                ////修改和替换配置     已经配置好的修改   例如下面修改  安全拦截器的安全数据源
                .withObjectPostProcessor(new ObjectPostProcessor<FilterSecurityInterceptor>() {
                    public <O extends FilterSecurityInterceptor> O postProcess(
                            O fsi) {
                        fsi.setPublishAuthorizationSuccess(true);
                        //修改成自定义的     安全元数据源  权限的源  ！！！！！
                        fsi.setSecurityMetadataSource(myInvocationSecurityMetadataSourceService);
                        //修改成自定义的     访问决策器  自定义的
                        fsi.setAccessDecisionManager(myAccessDecisionManager);
                        //使用系统的
                        fsi.setAuthenticationManager(authenticationManager);
                        return fsi;
                    }
                });
        /**
         *  请求认证管理
         */
        http.authorizeRequests()
                .antMatchers("url匹配路径").permitAll()          //url匹配路径 permitAll 运行 全部访问 不用认证
                .accessDecisionManager(null)                                 //访问决策器
                .filterSecurityInterceptorOncePerRequest(true)               //过滤每个请求一次的安全拦截器 ？？？
                .anyRequest().authenticated()                                //其他的请求 需要认证，
                .antMatchers("/admin/**").hasRole("ADMIN")      //url匹配路径  具有怎样的角色
                .antMatchers("/admin/**").access("hasRole('ROLE_ADMIN')")   //url匹配路径    具有怎样的角色 或者是权限
        ;
        /**
         *  anonymous
         *
         *  匿名访问时  存在默认 用户名  annonymousUser
         */
        http.anonymous().disable().csrf().disable();                         //禁止匿名  关闭csrf
        /**
         * 登出操作管理
         */
        http.logout()                                                        //登出处理
                .logoutUrl("/my/logout")
                .logoutSuccessUrl("/my/index")
                .logoutSuccessHandler(null)
                .invalidateHttpSession(true)
                .addLogoutHandler(null)
                .deleteCookies("cookieNamesToClear")
        ;
        /**
         *  session  会话管理
         */
        http.sessionManagement()                                            //session管理
                .maximumSessions(2)                                         //最大session 数量 --用户
                .maxSessionsPreventsLogin(false)                            //超过最大sessin数量后时候阻止登录
                .expiredUrl("/")                                            //会话失效后跳转的url
                .expiredSessionStrategy(null)                               //自定义session 过期错略
                .sessionRegistry(null)                                     //自定义的session 注册 表
        ;

    }

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        /**
         *   基础的配置
         */
        auth
                /**
                 * 认证 时触发的事件
                 */
                .authenticationEventPublisher(null)
                /**
                 *  用户细节服务
                 *
                 *  认证管理器数据的来源 吧  用户身份凭证信息和 权限信息
                 */
                .userDetailsService(null)
                /**
                 *  密码编辑器 对密码进行加密
                 */
                .passwordEncoder(null)
        ;
    }

    @Bean
    @Override
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }

    @Override
    public void configure(WebSecurity web) throws Exception {
        /**
         * 不进行拦截的mvc
         */
        web.ignoring().mvcMatchers();
        /**
         * 添加自定义的 安全过滤器
         */
        web.addSecurityFilterChainBuilder(null);
    }
}
```