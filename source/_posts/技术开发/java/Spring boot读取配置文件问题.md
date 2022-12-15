#### 1. 加载自定义文件

> YAML files cannot be loaded by using the @PropertySource annotation. So, in the case that you need to load values that way, you need to use a properties file.
> 即@PropertySource不支持YAML文件。

要让@PropertySource支持Yaml文件，可以做如下配置：

继承DefaultPropertySourceFactory类并修改

```java
public class YamlConfigFactory extends DefaultPropertySourceFactory {

    @Override
    public PropertySource<?> createPropertySource(String name, EncodedResource resource) throws IOException {
        String sourceName = name != null ? name : resource.getResource().getFilename();
        if (!resource.getResource().exists()) {
            return new PropertiesPropertySource(sourceName, new Properties());
        } else if (sourceName.endsWith(".yml") || sourceName.endsWith(".yaml")) {
            Properties propertiesFromYaml = loadYml(resource);
            return new PropertiesPropertySource(sourceName, propertiesFromYaml);
        } else {
            return super.createPropertySource(name, resource);
        }
    }

    private Properties loadYml(EncodedResource resource) throws IOException {
        YamlPropertiesFactoryBean factory = new YamlPropertiesFactoryBean();
        factory.setResources(resource.getResource());
        factory.afterPropertiesSet();
        return factory.getObject();
    }
}
```

配置注解：

```java
@PropertySource(value = {"classpath:application-my.yml"},factory = YamlConfigFactory.class)
```

#### 2. spring boot中配置文件访问优先级

优先级如下

1. 第一种是在执行命令的目录下建config文件夹，然后把配置文件放到这个文件夹下。(在jar包的同一个目录下建config文件夹，执行命令需要在jar包所在目录下才行)
2. 第二种是直接把配置文件放到jar包的同级目录
3. 第三种在classpath下建一个config文件夹，然后把配置文件放进去。
4. 第四种是在classpath下直接放配置文件。

springboot默认是优先读取它本身同级目录下的一个config/application.properties文件的。在src/main/resource文件夹下创建的application.properties文件的优先级是最低的

所以springboot启动读取外部配置文件，只需要在外面加一层配置文件覆盖默认的即可，不用修改代码

#### 3. 指定配置文件路径启动程序

\#通过 --spring.config.location指定配置文件路径

```java
nohup java -Xms256M -Xmx1024M -jar  mailgateway-2.0.0.12.jar --spring.config.location=/usr/ums_chenly/application-prod.properties --spring.profiles.active=prod > mailgateway_nohup_out_`date +%Y%m%d`.txt 2>&1 &
```

说明

1. 如果启动程序时指定配置文件路径，则程序运行时只读取指定的配置文件。指定配置文件不存在则报错，程序启动失败。
2. 如果不指定配置文件路径，则按上述优先级加载，如果优先级高的配置文件中没有某个配置项，则会到优先级低的配置文件中找该配置项，即具有互补功能(文件名相同才会互补，比如classpath下的application-prod.properties会补jar包的同级目录下application-prod.properties的某个配置项，但是classpath下的application.properties不会补application-prod.properties的某个配置项)。如果指定配置文件路径，则不互补，只会读取指定的配置文件。
3. 如果spring.config.location和 spring.profiles.active都不指定， 默认找application.properties文件。如果spring.profiles.active指定dev，则默认找application-dev.properties文件。如果spring.profiles.active指定prod,则会找application-prod.properties文件