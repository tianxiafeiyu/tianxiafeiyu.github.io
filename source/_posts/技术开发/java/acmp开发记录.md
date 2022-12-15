#### 1. 数据库存储创建日期是Instant格式，后台需要根据今天日期查找今天创建的记录。主要是需要得到Instant格式的今天的最小日期，用于比对。

```java
LocalDate localDate = LocalDate.now();
LocalDateTime minTime = localDate.atTime(LocalTime.MIN);
Instant today = minTime.toInstant(ZoneOffset.of("+0"));
```



#### 2. 物理分页查询（数据库分页）

业务场景：查询数据库表联系人分页，筛选条件pid、status、name；按创建时间降序排序。

```java
Specification<AlarmContact> specification = (Specification<AlarmContact>) (root, query, criteriaBuilder) -> {
            List<Predicate> list = new ArrayList<>();
            list.add(criteriaBuilder.equal(root.get("projectId"), projectId));
            list.add(criteriaBuilder.equal(root.get("status"), ResourceStatus.ENABLE));
            if (name.length() != 0) {
                // 此处为查询含有name的数据
                list.add(criteriaBuilder.like(root.get("name"),"%"+ name +"%" ));
            }
            Predicate[] p = new Predicate[list.size()];
            return criteriaBuilder.and(list.toArray(p));
        };
Pageable pageable = new PageRequest(page, limit, Sort.Direction.DESC, "createdDate");
Page<AlarmContact> alarmContact，Page = alarmContactRepository.findAll(specification, pageable);
```



#### 3. 集合分页

业务场景：拥有用户的集合，需要将这个集合进行分页返回给前端。

```java
List<User> userList;//默认已经有List数据
//根据传进来的用户名字进行模糊筛选
        if(0 != name.length()){
            List<User> temList = new ArrayList<>();
            temList.addAll(userList);
            for(User user : temList){
                if(!user.getUsername().contains(name)){
                    userList.remove(user);
                }
            }
        }
//集合转Page
Pageable pageable = new PageRequest(page, limit, Sort.Direction.ASC, "id");
// 当前页第一条数据在List中的位置
int start = (int)pageable.getOffset();
// 当前页最后一条数据在List中的位置
int end = (start + pageable.getPageSize()) > userList.size() ? userList.size() : ( start + pageable.getPageSize());
// 配置分页数据
Page<User> userPagePage = new PageImpl<>(userList.subList(start, end), pageable, userList.size());
```



#### 4. 树的相关操作

业务场景：在做权限控制的时候，权限是树的形式，根据前端需求需要提供不同的数据格式。

1. 求出当前用户的所有具体权限（叶子节点）

```java
public Set<Permission> getEXactPermission() {
    Set<Role> roles = userRoleRepository.findByUserId(userCache.getId()).stream().map(userRole -> userRole.getRole()).collect(Collectors.toSet());
    Set<Permission> permissions = roles.stream().flatMap(role -> role.getPermissions().stream()).collect(Collectors.toSet());
    Set<Permission> exactPermissions = new HashSet<>();
    for(Permission permission : permissions){
    Set<Permission> permissions1 = new HashSet<>();
    findTreeleafs(permission, permissions1);
    exactPermissions.addAll(permissions1);
    }
    return exactPermissions;
}


//递归遍历树的叶子节点，如果只有一个节点，它也是叶子
public void findTreeleafs(Permission permission, Set<Permission> permissionSet) {
    if(permission.getChildren().size() == 0){
        permissionSet.add(permission);
    }
    for(Permission permission1 : permission.getChildren()){
        if (permission.getChildren().size() == 0) {
            permissionSet.addAll(permission.getChildren());
        } else {
            findTreeleafs(permission1, permissionSet);
        }
    }
}
```

2) 获取权限子树。就是用户拥有权限的完整路径

思路：获取用户的具体权限集合（叶子节点），删除完整树中没有达到集合中的路径。



#### 5. spring boot JPA多条件查询

1）Repository需要继承JpaRepository和JpaSpecificationExecutor

```java
public interface projectRepository extends JpaRepository<Project, Long>, JpaSpecificationExecutor<Project> {
    
}
```

2）构建筛选器

```java
 /**
     * 分页查询获取分页列表
     * @param companyId
     * @return
     */
    public Page<Project> getListByCompanyPage(PageFilter pageFilter,String companyId,Date beginDate,Date endDate,String projectName) {
        Page<Project> l=projectRepository.findAll(new Specification<Project>() {
            @Override
            public Predicate toPredicate(Root<Project> root, CriteriaQuery<?> criteriaQuery, CriteriaBuilder cBuilder) {
                //开始，定义一个Predicate
                Predicat  e p = cBuilder.conjunction();
                /**精确查询**/
                p = cBuilder.and(p, cBuilder.equal(root.get("companyId"), companyId));
                /**模糊查询**/
                p = cBuilder.and(p, cBuilder.like(root.get("projectName"), "%"+projectName+"%"));
                /**时间段查询**/
                //大于等于开始时间
                p = cBuilder.and(p, cBuilder.greaterThanOrEqualTo(root.get("createTime"), beginDate));
                //小于等于结束时间
                p = cBuilder.and(p, cBuilder.lessThanOrEqualTo(root.get("createTime"), endDate));
                return p;
            }
        }, pageFilter.getPageRequest());
        return l;
```



#### 6. jpa delete无法删除

问题描述：两张表表1和表2通过一张中间表表3关联，都是一对多关系。表1的一条记录 a 已经和表2的记录 b 关联起来了。逻辑删除 a 记录，现在需要删除 b 记录，表3的关联记录还存在，要先根据 b 记录删掉表3的关联记录，但是此时用 JPA 的 deleteAllBy... 不生效，非常疑惑，自定义 sql 删除生效。

```java
@Modifying
@Query("delete from UserRole where role.id = ?1")
```

解答：看到网上有说法说是 JPA 的 entity 对象生命周期问题，由于表 1 还存在记录的引用，之后会更新回来。。。



#### 7. 分页查询结果集中某个属性等于某个值的元素排在前面

业务场景：分页查询数据库，状态为 ON 的值排在前面，且根据最后修改时间排序。

分析讨论：Java分页查询的排序并不是很难，特别是使用Pagable时排序非常方便，但是一般的排序都市按照升序或者降序排序，根据某个属性的特定值排序很少看见，头疼。

问题解决：

1）偷懒办法，如果只有两种状态，仍然可以用升序降序进行排序，这时候比较的就是两种不同值的相对大小（数值、字符串类型等）；

```java
Sort sort =new Sort(Sort.Direction.DESC, "status").and(new Sort(Sort.Direction.DESC, "lastModifiedDate"));
Pageable pageable = new PageRequest(page, limit, sort);
```



2）有多种不同状态时，可以使用 sql 语句进行查询 

3）查询出元素集合列表，进行排序，然后对集合进行分页。



#### 8. 读取 jar 包中MANIFEST.MF文件信息

```java
// 通过JarFile的getJarEntry方法读取META-INF/MANIFEST.MF
jarFile = new JarFile(jarFilePath);
JarEntry entry = jarFile.getJarEntry("META-INF/MANIFEST.MF");
// 如果读取到MANIFEST.   F文件内容，则转换为string
if (entry != null) {
    InputStream in =  jarFile.getInputStream(entry);
    StringBuilder sb = new StringBuilder();
    BufferedReader br = new BufferedReader(new InputStreamReader(in));
    String line = "";
    while ((line = br.readLine()) != null) {
        sb.append(line+"<br>");
    }
```



#### 9. 编写泛型方法

错误示例：

```java
public static Page<T> getPage(int page, int limit, List<T> data){    // ... }
```

实际使用时候会报类型无法匹配的错误。

正确写法：

```java
public static <T extends Object> Page<T> getPage(int page, int limit, List<T> data){
    // ...
}
```



#### 10. Java中父类能不能强转为子类？

一般来说父类是不能强转为子类对象的，因为子类中可能包含父类没有的属性或方法，父类强转子类会存在不确定性。

> 《java面向对象程序设计（第2版）》，一个父类类型的对象如果是用子类new出来的时候, 就不能称之为父类对象，而是一个子类的上转型对象。这两者是有区别的，区别的其中一点就是父类对象不可强制转换为子类对象，而子类的上转型对象可以强制转换回子类对象

```java
class Father{
    
}
class Son extends Father{
    
}
public class Main{
    public static void main(String[] args){
        Father father1 = new Father();
       Father father2 = new Son();
       Son son1 = (Son) father1;//报错
       Son son2 = (Son) father2;//不报错
    }
}
```

网上看到很搞笑的一段描述：孙子可能会装大爷，大爷永远不会装孙子。

哈哈，非常贴切生动了。