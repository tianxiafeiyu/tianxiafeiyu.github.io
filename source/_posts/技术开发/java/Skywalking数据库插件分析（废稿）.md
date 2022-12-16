---
title: Skywalking数据库插件分析（废稿）
date: 2022-12-15 23:39:56
updated: 2022-12-16 21:36:16
toc: true
tags: 
    - Skywalking数据库插件分析（废稿）
---
# apm-mysql-8.x-plugin
## 主要增强的功能有：
```
//
mysql-8.x=org.apache.skywalking.apm.plugin.jdbc.mysql.v8.define.ConnectionImplCreateInstrumentation 
mysql-8.x=org.apache.skywalking.apm.plugin.jdbc.mysql.v8.define.ConnectionInstrumentation
mysql-8.x=org.apache.skywalking.apm.plugin.jdbc.mysql.v8.define.CallableInstrumentation
mysql-8.x=org.apache.skywalking.apm.plugin.jdbc.mysql.v8.define.PreparedStatementInstrumentation
mysql-8.x=org.apache.skywalking.apm.plugin.jdbc.mysql.v8.define.StatementInstrumentation
mysql-8.x=org.apache.skywalking.apm.plugin.jdbc.mysql.v8.define.PreparedStatementSetterInstrumentation
mysql-8.x=org.apache.skywalking.apm.plugin.jdbc.mysql.v8.define.PreparedStatementNullSetterInstrumentation
mysql-8.x=org.apache.skywalking.apm.plugin.jdbc.mysql.v8.define.PreparedStatementIgnoredSetterInstrumentation
```

## 源码分析
### ConnectionCreateInterceptor.class
```java
import com.mysql.cj.conf.HostInfo;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.enhance.EnhancedInstance;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.enhance.MethodInterceptResult;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.enhance.StaticMethodsAroundInterceptor;
import org.apache.skywalking.apm.plugin.jdbc.connectionurl.parser.URLParser;
import org.apache.skywalking.apm.plugin.jdbc.trace.ConnectionInfo;

import java.lang.reflect.Method;

public class ConnectionCreateInterceptor implements StaticMethodsAroundInterceptor {

    @Override
    public void beforeMethod(Class clazz, Method method, Object[] allArguments, Class<?>[] parameterTypes,
        MethodInterceptResult result) {

    }

    @Override
    public Object afterMethod(Class clazz, Method method, Object[] allArguments, Class<?>[] parameterTypes,
        Object ret) {
        if (ret instanceof EnhancedInstance) {
            final HostInfo hostInfo = (HostInfo) allArguments[0];
            ConnectionInfo connectionInfo = URLParser.parser(hostInfo.getDatabaseUrl());
            ((EnhancedInstance) ret).setSkyWalkingDynamicField(connectionInfo);
        }
        return ret;
    }

    @Override
    public void handleMethodException(Class clazz, Method method, Object[] allArguments, Class<?>[] parameterTypes,
        Throwable t) {

    }
}
```
- ConnectionCreateInterceptor实现了StaticMethodsAroundInterceptor接口，
- afterMethod方法提取com.mysql.cj.conf.HostInfo解析为org.apache.skywalking.apm.plugin.jdbc.trace.ConnectionInfo
- 设置给ret的skyWalkingDynamicField，记录连接信息

### AbstractMysqlInstrumentation
```java
package org.apache.skywalking.apm.plugin.jdbc.mysql.v8.define;

import org.apache.skywalking.apm.agent.core.plugin.interceptor.ConstructorInterceptPoint;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.InstanceMethodsInterceptPoint;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.StaticMethodsInterceptPoint;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.enhance.ClassEnhancePluginDefine;

public abstract class AbstractMysqlInstrumentation extends ClassEnhancePluginDefine {

    @Override
    public ConstructorInterceptPoint[] getConstructorsInterceptPoints() {
        return null;
    }

    @Override
    public StaticMethodsInterceptPoint[] getStaticMethodsInterceptPoints() {
        return null;
    }

    @Override
    public InstanceMethodsInterceptPoint[] getInstanceMethodsInterceptPoints() {
        return null;
    }

    @Override
    protected String[] witnessClasses() {
        return new String[] {Constants.WITNESS_MYSQL_8X_CLASS};
    }
}
```
- AbstractMysqlInstrumentation继承了ClassEnhancePluginDefine，定义了构造器方法、静态方法、实例方法的拦截形式。
- witnessClasses返回的是com.mysql.cj.interceptors.QueryInterceptor

### CallableInstrumentation
```java
package org.apache.skywalking.apm.plugin.jdbc.mysql.v8.define;

import net.bytebuddy.description.method.MethodDescription;
import net.bytebuddy.matcher.ElementMatcher;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.ConstructorInterceptPoint;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.InstanceMethodsInterceptPoint;
import org.apache.skywalking.apm.agent.core.plugin.match.ClassMatch;

import static net.bytebuddy.matcher.ElementMatchers.named;
import static org.apache.skywalking.apm.agent.core.plugin.match.NameMatch.byName;

public class CallableInstrumentation extends AbstractMysqlInstrumentation {
    private static final String ENHANCE_CLASS = "com.mysql.cj.jdbc.CallableStatement";
    private static final String SERVICE_METHOD_INTERCEPTOR = org.apache.skywalking.apm.plugin.jdbc.mysql.Constants.PREPARED_STATEMENT_EXECUTE_METHODS_INTERCEPTOR;

    @Override
    public ConstructorInterceptPoint[] getConstructorsInterceptPoints() {
        return new ConstructorInterceptPoint[0];
    }

    @Override
    public InstanceMethodsInterceptPoint[] getInstanceMethodsInterceptPoints() {
        return new InstanceMethodsInterceptPoint[] {
            new InstanceMethodsInterceptPoint() {
                @Override
                public ElementMatcher<MethodDescription> getMethodsMatcher() {
                    return named("execute").or(named("executeQuery")).or(named("executeUpdate"));
                }

                @Override
                public String getMethodsInterceptor() {
                    return SERVICE_METHOD_INTERCEPTOR;
                }

                @Override
                public boolean isOverrideArgs() {
                    return false;
                }
            }
        };
    }

    @Override
    protected ClassMatch enhanceClass() {
        return byName(ENHANCE_CLASS);
    }

}
```
- 增强com.mysql.cj.jdbc.CallableStatement类，即调用过程
- 定义该类实例方法的拦截形式，匹配“execute”或“executeQuery”或“executeUpdate”方法
- 指定该实例方法的拦截器org.apache.skywalking.apm.plugin.jdbc.mysql.PreparedStatementExecuteMethodsInterceptor
- 不重写实例方法参数

### PreparedStatementExecuteMethodsInterceptor
```java
package org.apache.skywalking.apm.plugin.jdbc.mysql;

import java.lang.reflect.Method;
import org.apache.skywalking.apm.agent.core.context.ContextManager;
import org.apache.skywalking.apm.agent.core.context.tag.Tags;
import org.apache.skywalking.apm.agent.core.context.trace.AbstractSpan;
import org.apache.skywalking.apm.agent.core.context.trace.SpanLayer;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.enhance.EnhancedInstance;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.enhance.InstanceMethodsAroundInterceptor;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.enhance.MethodInterceptResult;
import org.apache.skywalking.apm.plugin.jdbc.JDBCPluginConfig;
import org.apache.skywalking.apm.plugin.jdbc.PreparedStatementParameterBuilder;
import org.apache.skywalking.apm.plugin.jdbc.define.StatementEnhanceInfos;
import org.apache.skywalking.apm.plugin.jdbc.trace.ConnectionInfo;

import static org.apache.skywalking.apm.plugin.jdbc.mysql.Constants.SQL_PARAMETERS;

public class PreparedStatementExecuteMethodsInterceptor implements InstanceMethodsAroundInterceptor {

    @Override
    public final void beforeMethod(EnhancedInstance objInst, Method method, Object[] allArguments,
                                   Class<?>[] argumentsTypes, MethodInterceptResult result) {
        StatementEnhanceInfos cacheObject = (StatementEnhanceInfos) objInst.getSkyWalkingDynamicField();
        /**
         * For avoid NPE. In this particular case, Execute sql inside the {@link com.mysql.jdbc.ConnectionImpl} constructor,
         * before the interceptor sets the connectionInfo.
         * When invoking prepareCall, cacheObject is null. Because it will determine procedures's parameter types by executing sql in mysql 
         * before the interceptor sets the statementEnhanceInfos.
         * @see JDBCDriverInterceptor#afterMethod(EnhancedInstance, Method, Object[], Class[], Object)
         */
        if (cacheObject != null && cacheObject.getConnectionInfo() != null) {
            ConnectionInfo connectInfo = cacheObject.getConnectionInfo();
            AbstractSpan span = ContextManager.createExitSpan(
                buildOperationName(connectInfo, method.getName(), cacheObject
                    .getStatementName()), connectInfo.getDatabasePeer());
            Tags.DB_TYPE.set(span, "sql");
            Tags.DB_INSTANCE.set(span, connectInfo.getDatabaseName());
            Tags.DB_STATEMENT.set(span, cacheObject.getSql());
            span.setComponent(connectInfo.getComponent());

            if (JDBCPluginConfig.Plugin.MySQL.TRACE_SQL_PARAMETERS) {
                final Object[] parameters = cacheObject.getParameters();
                if (parameters != null && parameters.length > 0) {
                    int maxIndex = cacheObject.getMaxIndex();
                    String parameterString = getParameterString(parameters, maxIndex);
                    SQL_PARAMETERS.set(span, parameterString);
                }
            }

            SpanLayer.asDB(span);
        }
    }

    @Override
    public final Object afterMethod(EnhancedInstance objInst, Method method, Object[] allArguments,
                                    Class<?>[] argumentsTypes, Object ret) {
        StatementEnhanceInfos cacheObject = (StatementEnhanceInfos) objInst.getSkyWalkingDynamicField();
        if (cacheObject != null && cacheObject.getConnectionInfo() != null) {
            ContextManager.stopSpan();
        }
        return ret;
    }

    @Override
    public final void handleMethodException(EnhancedInstance objInst, Method method, Object[] allArguments,
                                            Class<?>[] argumentsTypes, Throwable t) {
        StatementEnhanceInfos cacheObject = (StatementEnhanceInfos) objInst.getSkyWalkingDynamicField();
        if (cacheObject != null && cacheObject.getConnectionInfo() != null) {
            ContextManager.activeSpan().errorOccurred().log(t);
        }
    }

    private String buildOperationName(ConnectionInfo connectionInfo, String methodName, String statementName) {
        return connectionInfo.getDBType() + "/JDBI/" + statementName + "/" + methodName;
    }

    private String getParameterString(Object[] parameters, int maxIndex) {
        return new PreparedStatementParameterBuilder()
            .setParameters(parameters)
            .setMaxIndex(maxIndex)
            .setMaxLength(JDBCPluginConfig.Plugin.MySQL.SQL_PARAMETERS_MAX_LENGTH)
            .build();
    }
}
```
- beforeMethod：创建ExitSpan，记录DB_TYPE、DB_INSTANCE、DB_STATEMENT等信息 如果开启参数追踪，记录参数信息
- afterMethod：结束此Span追踪
- handleMethodException：当前方法出现异常，将堆栈信息存入此Span

### ConnectionImplCreateInstrumentation
```
package org.apache.skywalking.apm.plugin.jdbc.mysql.v8.define;

import net.bytebuddy.description.method.MethodDescription;
import net.bytebuddy.matcher.ElementMatcher;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.StaticMethodsInterceptPoint;
import org.apache.skywalking.apm.agent.core.plugin.match.ClassMatch;

import java.util.Properties;

import static net.bytebuddy.matcher.ElementMatchers.named;
import static org.apache.skywalking.apm.agent.core.plugin.match.NameMatch.byName;

/**
 * interceptor the method {@link com.mysql.cj.jdbc.ConnectionImpl#getInstance(com.mysql.cj.conf.HostInfo)} instead of
 * {@link com.mysql.cj.jdbc.Driver#connect(String, Properties)}
 */
public class ConnectionImplCreateInstrumentation extends AbstractMysqlInstrumentation {

    private static final String JDBC_ENHANCE_CLASS = "com.mysql.cj.jdbc.ConnectionImpl";

    private static final String CONNECT_METHOD = "getInstance";

    @Override
    public StaticMethodsInterceptPoint[] getStaticMethodsInterceptPoints() {
        return new StaticMethodsInterceptPoint[] {
            new StaticMethodsInterceptPoint() {
                @Override
                public ElementMatcher<MethodDescription> getMethodsMatcher() {
                    return named(CONNECT_METHOD);
                }

                @Override
                public String getMethodsInterceptor() {
                    return "org.apache.skywalking.apm.plugin.jdbc.mysql.v8.ConnectionCreateInterceptor";
                }

                @Override
                public boolean isOverrideArgs() {
                    return false;
                }
            }
        };
    }

    @Override
    protected ClassMatch enhanceClass() {
        return byName(JDBC_ENHANCE_CLASS);
    }
}
```
- 增强com.mysql.cj.jdbc.ConnectionImpl类
- 指定增强该类的getInstance静态方法
- 指定静态方法拦截器org.apache.skywalking.apm.plugin.jdbc.mysql.v8.ConnectionCreateInterceptor
- 不重写方法参数

### ConnectionCreateInterceptor
```java
package org.apache.skywalking.apm.plugin.jdbc.mysql.v8;

import com.mysql.cj.conf.HostInfo;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.enhance.EnhancedInstance;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.enhance.MethodInterceptResult;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.enhance.StaticMethodsAroundInterceptor;
import org.apache.skywalking.apm.plugin.jdbc.connectionurl.parser.URLParser;
import org.apache.skywalking.apm.plugin.jdbc.trace.ConnectionInfo;

import java.lang.reflect.Method;

public class ConnectionCreateInterceptor implements StaticMethodsAroundInterceptor {

    @Override
    public void beforeMethod(Class clazz, Method method, Object[] allArguments, Class<?>[] parameterTypes,
        MethodInterceptResult result) {

    }

    @Override
    public Object afterMethod(Class clazz, Method method, Object[] allArguments, Class<?>[] parameterTypes,
        Object ret) {
        if (ret instanceof EnhancedInstance) {
            final HostInfo hostInfo = (HostInfo) allArguments[0];
            ConnectionInfo connectionInfo = URLParser.parser(hostInfo.getDatabaseUrl());
            ((EnhancedInstance) ret).setSkyWalkingDynamicField(connectionInfo);
        }
        return ret;
    }

    @Override
    public void handleMethodException(Class clazz, Method method, Object[] allArguments, Class<?>[] parameterTypes,
        Throwable t) {

    }
}
```
- afterMethod：方法执行完成后，记录当前方法的数据库连接信息

### ConnectionInstrumentation
```java
package org.apache.skywalking.apm.plugin.jdbc.mysql.v8.define;

import net.bytebuddy.description.method.MethodDescription;
import net.bytebuddy.matcher.ElementMatcher;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.ConstructorInterceptPoint;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.InstanceMethodsInterceptPoint;
import org.apache.skywalking.apm.agent.core.plugin.match.ClassMatch;

import static net.bytebuddy.matcher.ElementMatchers.named;
import static net.bytebuddy.matcher.ElementMatchers.takesArguments;
import static org.apache.skywalking.apm.agent.core.plugin.match.NameMatch.byName;

public class ConnectionInstrumentation extends AbstractMysqlInstrumentation {

    @Override
    public ConstructorInterceptPoint[] getConstructorsInterceptPoints() {
        return new ConstructorInterceptPoint[0];
    }

    @Override
    public InstanceMethodsInterceptPoint[] getInstanceMethodsInterceptPoints() {
        return new InstanceMethodsInterceptPoint[] {
            new InstanceMethodsInterceptPoint() {
                @Override
                public ElementMatcher<MethodDescription> getMethodsMatcher() {
                    return named(org.apache.skywalking.apm.plugin.jdbc.define.Constants.PREPARE_STATEMENT_METHOD_NAME);
                }

                @Override
                public String getMethodsInterceptor() {
                    return org.apache.skywalking.apm.plugin.jdbc.mysql.Constants.CREATE_PREPARED_STATEMENT_INTERCEPTOR;
                }

                @Override
                public boolean isOverrideArgs() {
                    return false;
                }
            },
            new InstanceMethodsInterceptPoint() {
                @Override
                public ElementMatcher<MethodDescription> getMethodsMatcher() {
                    return named(org.apache.skywalking.apm.plugin.jdbc.define.Constants.PREPARE_CALL_METHOD_NAME);
                }

                @Override
                public String getMethodsInterceptor() {
                    return org.apache.skywalking.apm.plugin.jdbc.mysql.Constants.CREATE_CALLABLE_STATEMENT_INTERCEPTOR;
                }

                @Override
                public boolean isOverrideArgs() {
                    return false;
                }
            },
            new InstanceMethodsInterceptPoint() {
                @Override
                public ElementMatcher<MethodDescription> getMethodsMatcher() {
                    return named(org.apache.skywalking.apm.plugin.jdbc.define.Constants.CREATE_STATEMENT_METHOD_NAME).and(takesArguments(2));
                }

                @Override
                public String getMethodsInterceptor() {
                    return org.apache.skywalking.apm.plugin.jdbc.mysql.Constants.CREATE_STATEMENT_INTERCEPTOR;
                }

                @Override
                public boolean isOverrideArgs() {
                    return false;
                }
            },
            new InstanceMethodsInterceptPoint() {
                @Override
                public ElementMatcher<MethodDescription> getMethodsMatcher() {
                    return named(org.apache.skywalking.apm.plugin.jdbc.define.Constants.COMMIT_METHOD_NAME).or(named(org.apache.skywalking.apm.plugin.jdbc.define.Constants.ROLLBACK_METHOD_NAME))
                                                                                                           .or(named(org.apache.skywalking.apm.plugin.jdbc.define.Constants.CLOSE_METHOD_NAME))
                                                                                                           .or(named(org.apache.skywalking.apm.plugin.jdbc.define.Constants.RELEASE_SAVE_POINT_METHOD_NAME));
                }

                @Override
                public String getMethodsInterceptor() {
                    return org.apache.skywalking.apm.plugin.jdbc.define.Constants.SERVICE_METHOD_INTERCEPT_CLASS;
                }

                @Override
                public boolean isOverrideArgs() {
                    return false;
                }
            },
            new InstanceMethodsInterceptPoint() {
                @Override
                public ElementMatcher<MethodDescription> getMethodsMatcher() {
                    return named("setCatalog");
                }

                @Override
                public String getMethodsInterceptor() {
                    return org.apache.skywalking.apm.plugin.jdbc.mysql.Constants.SET_CATALOG_INTERCEPTOR;
                }

                @Override
                public boolean isOverrideArgs() {
                    return false;
                }
            }
        };

    }

    @Override
    protected ClassMatch enhanceClass() {
        return byName("com.mysql.cj.jdbc.ConnectionImpl");
    }
}
```
- 指定要增强的类com.mysql.cj.jdbc.ConnectionImpl
- 定义构造方法的拦截形式
- 定义实例方法的拦截形式：
    1. 拦截prepareStatement方法
        - 指定拦截器org.apache.skywalking.apm.plugin.jdbc.mysql.CreatePreparedStatementInterceptor
        - 不重写方法参数
    2. 拦截prepareCall方法
        - 指定拦截器org.apache.skywalking.apm.plugin.jdbc.mysql.CreateCallableStatementInterceptor
        - 不重写方法参数
    3. 拦截createStatement方法
        - 指定拦截器org.apache.skywalking.apm.plugin.jdbc.mysql.CreateStatementInterceptor
        - 不重写方法参数
    4. 拦截commit或rollback或close或releaseSavepoint方法
        - 指定拦截器org.apache.skywalking.apm.plugin.jdbc.ConnectionServiceMethodInterceptor
        - 不重写方法参数
    5. 拦截setCatalog方法
        - 指定拦截器org.apache.skywalking.apm.plugin.jdbc.mysql.SetCatalogInterceptor
        - 不重写参数

### CreatePreparedStatementInterceptor
```java
package org.apache.skywalking.apm.plugin.jdbc.mysql;

import org.apache.skywalking.apm.agent.core.plugin.interceptor.enhance.EnhancedInstance;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.enhance.InstanceMethodsAroundInterceptor;
import org.apache.skywalking.apm.agent.core.plugin.interceptor.enhance.MethodInterceptResult;
import org.apache.skywalking.apm.plugin.jdbc.define.StatementEnhanceInfos;
import org.apache.skywalking.apm.plugin.jdbc.trace.ConnectionInfo;

import java.lang.reflect.Method;

public class CreatePreparedStatementInterceptor implements InstanceMethodsAroundInterceptor {
    @Override
    public void beforeMethod(EnhancedInstance objInst, Method method, Object[] allArguments, Class<?>[] argumentsTypes,
        MethodInterceptResult result) throws Throwable {
    }

    @Override
    public Object afterMethod(EnhancedInstance objInst, Method method, Object[] allArguments, Class<?>[] argumentsTypes,
        Object ret) throws Throwable {
        if (ret instanceof EnhancedInstance) {
            // allArguments[0]为要执行的sql，设置到ret的SkyWalkingDynamicField
            ((EnhancedInstance) ret).setSkyWalkingDynamicField(new StatementEnhanceInfos((ConnectionInfo) objInst.getSkyWalkingDynamicField(), (String) allArguments[0], "PreparedStatement"));
        }
        return ret;
    }

    @Override
    public void handleMethodException(EnhancedInstance objInst, Method method, Object[] allArguments,
        Class<?>[] argumentsTypes, Throwable t) {

    }
}
```
- afterMethod：实例方法结束后，创建StatementEnhanceInfos

