---
title: Prometheus监控kubernetes方案及实现
---

# promtheus监控kubernetes
## Kubernetes监控策略
Kubernetes作为开源的容器编排工具，为用户提供了一个可以统一调度，统一管理的云操作系统。其解决如用户应用程序如何运行的问题。而一旦在生产环境中大量基于Kubernetes部署和管理应用程序后，作为系统管理员，还需要充分了解应用程序以及Kubernetes集群服务运行质量如何，通过对应用以及集群运行状态数据的收集和分析，持续优化和改进，从而提供一个安全可靠的生产运行环境。这一小节中我们将讨论当使用Kubernetes时的监控策略该如何设计。  

从物理结构上讲Kubernetes主要用于整合和管理底层的基础设施资源，对外提供应用容器的自动化部署和管理能力，这些基础设施可能是物理机、虚拟机、云主机等等。因此，基础资源的使用直接影响当前集群的容量和应用的状态。在这部分，我们需要关注集群中各个节点的主机负载，CPU使用率、内存使用率、存储空间以及网络吞吐等监控指标。  

从自身架构上讲，kube-apiserver是Kubernetes提供所有服务的入口，无论是外部的客户端还是集群内部的组件都直接与kube-apiserver进行通讯。因此，kube-apiserver的并发和吞吐量直接决定了集群性能的好坏。其次，对于外部用户而言，Kubernetes是否能够快速的完成pod的调度以及启动，是影响其使用体验的关键因素。而这个过程主要由kube-scheduler负责完成调度工作，而kubelet完成pod的创建和启动工作。因此在Kubernetes集群本身我们需要评价其自身的服务质量，主要关注在Kubernetes的API响应时间，以及Pod的启动时间等指标上。  

Kubernetes的最终目标还是需要为业务服务，因此我们还需要能够监控应用容器的资源使用情况。对于内置了对Prometheus支持的应用程序，也要支持从这些应用程序中采集内部的监控指标。最后，结合黑盒监控模式，对集群中部署的服务进行探测，从而当应用发生故障后，能够快速处理和恢复。  

在Kubernetes集群上也需要监控Pod、DaemonSet、Deployment、Job、Cronjob等资源对象的状态，这样可以反映出使用这些资源部署的应用状态。但通过查看api-server或者cAdvisor的指标，并没有具体的各种资源对象的状态指标，对于Prometheus来说，当然需要引入新的exporter来暴露这些指标，Kubernetes提供了名为kube-state-metrics的项目（项目地址：https://github.com/kubernetes/kube-state-metrics ）。

综上所述，我们需要综合使用白盒监控和黑盒监控模式，建立从基础设施，Kubernetes核心组件，应用容器等全面的监控体系。  

在白盒监控层面我们需要关注：
- 基础设施层（Node）：为整个集群和应用提供运行时资源，需要通过各节点的kubelet获取节点的基本状态，同时通过在节点上部署Node Exporter获取节点的资源使用情况；
- 容器基础设施（Container）：为应用提供运行时环境，Kubelet内置了对cAdvisor的支持，用户可以直接通过Kubelet组件获取给节点上容器相关监控指标；
- 用户应用（Pod）：Pod中会包含一组容器，它们一起工作，并且对外提供一个（或者一组）功能。如果用户部署的应用程序内置了对Prometheus的支持，那么我们还应该采集这些Pod暴露的监控指标；
- Kubernetes组件：获取并监控Kubernetes核心组件的运行状态，确保平台自身的稳定运行。  
- Kubernetes资源对象：监控Pod、DaemonSet、Deployment、Job、Cronjob等资源对象的状态，反映出使用这些资源部署的应用状态

而在黑盒监控层面，则主要需要关注以下：
- 内部服务负载均衡（Service）：在集群内，通过Service在集群暴露应用功能，集群内应用和应用之间访问时提供内部的负载均衡。通过Balckbox Exporter探测Service的可用性，确保当Service不可用时能够快速得到告警通知；
- 外部访问入口（Ingress）：通过Ingress提供集群外的访问入口，从而可以使外部客户端能够访问到部署在Kubernetes集群内的服务。因此也需要通过Blackbox Exporter对Ingress的可用性进行探测，确保外部用户能够正常访问集群内的功能；



下表中，梳理了监控Kubernetes集群监控的各个维度以及策略：

 目标 | 描述 | 服务发现方式 | 监控方法 | 数据源 | 集群外监控
---|---|---|---|---| --- |
api-server | 获取API Server组件的访问地址，并从中获取Kubernetes集群相关的运行监控指标 | endpoints | 白盒监控 | api server |         ✓           | 
kube-schedule | kube-schedule的metrics接口 （Scheduler服务端口默认为10251）| - | 白盒监控 | kube-schedule |         ✓           | 
control-manager | control-manager的metrics接口（ControllerManager服务端口默认为10252）| - | 白盒监控 | control-manager |         ✓           | 
kubelet | 从集群各节点kubelet组件中获取节点kubelet的基本运行状态的监控指标 | node | 白盒监控 | kubelet |         ✓           | 
kube-proxy | kube-proxy的metrics接口（ControllerManager服务端口默认为10252）| - | 白盒监控 | kube-proxy |         ✓           | 
kube-dns | 从集群各节点获取kube-dns的基本运行状态的监控指标| - | 白盒监控 | kube-dns |         ✓           | 
cAdvisor | 从集群各节点kubelet内置的cAdvisor中获取，节点中运行的容器的监控指标 | node | 白盒监控 | kubelet |         ✓           | 
node | 从部署到各个节点的Node Exporter中采集主机资源相关的运行资源 | node | 白盒监控 | node exporter |         ✓           | 
pod | 对于内置了Promthues支持的应用，需要从Pod实例中采集其自定义监控指标 | pod | 白盒监控 | custom pod |         ✓           | 
资源对象 | 监控Pod、DaemonSet、Deployment、Job、Cronjob等资源对象的状态，反映出使用这些资源部署的应用状态 | endpoints | 白盒监控 | kube-state-metrics |         ✓           | 
service | 获取集群中Service的访问地址，并通过Blackbox  Exporter获取网络探测指标 | service | 黑盒监控 | blackbox exporter |                 ✓           | 
ingress | 获取集群中Ingress的访问信息，并通过Blackbox Exporter获取网络探测指标 | ingress | 黑盒监控 | blackbox exporter |                 ✓           | 


## kubernetes监控实现
使用prometheus监控kubernetes，基本上有两个场景： 
- prometheus部署在k8s集群内部；
- prometheus部署在k8s集群外部。  

两种场景大同小异，原理上都是基于kubernetes服务发现，promtheus自身已经实现了基于kubernetes的服务发现。但目前prometheus部署在k8s集群外部对于service和ingress的监控暂无合适方案


### prometheus部署在k8s集群外部监控实现

#### Kubernetes访问授权
为了能够让Prometheus能够访问收到认证保护的Kubernetes API，我们首先需要做的是，对Prometheus进行访问授权。在Kubernetes中主要使用基于角色的访问控制模型(Role-Based Access Control)，用于管理Kubernetes下资源访问权限。首先我们需要在Kubernetes下定义角色（ClusterRole），并且为该角色赋予响应的访问权限。同时创建Prometheus所使用的账号（ServiceAccount），最后则是将该账号与角色进行绑定（ClusterRoleBinding）。这些所有的操作在Kubernetes同样被视为是一系列的资源，可以通过YAML文件进行描述并创建，这里创建prometheus-rbac-setup.yml文件，并写入以下内容：
```
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRole
metadata:
  name: prometheus
rules:
- apiGroups: [""]
  resources:
  - nodes
  - nodes/proxy
  - services
  - services/proxy
  - endpoints
  - pods
  - pods/proxy
  verbs: ["get", "list", "watch"]
- apiGroups:
  - extensions
  resources:
  - ingresses
  verbs: ["get", "list", "watch"]
- nonResourceURLs: ["/metrics"]
  verbs: ["get"]
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: prometheus
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: prometheus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: prometheus
subjects:
- kind: ServiceAccount
  name: prometheus
  namespace: default
```

通过kubectl命令创建RBAC对应的各个资源：

```
$ kubectl create -f prometheus-rbac-setup.yml
clusterrole "prometheus" created
serviceaccount "prometheus" created
clusterrolebinding "prometheus" created
```

外部的prometheus需要获取Bearer Token来访问kubernetes api：

```
$ SECRET=$(kubectl get serviceaccount prometheus -ojsonpath='{.secrets[0].name}')
$ kubectl get secret ${SECRET} -o jsonpath="{.data.token}" | base64 -d > /tmp/prometheus-sa-token
```

#### 从kube-apiserver获取集群运行监控指标
kube-apiserver扮演了整个Kubernetes集群管理的入口的角色，负责对外暴露Kubernetes API。kube-apiserver组件一般是独立部署在集群外的，为了能够让部署在集群内的应用（kubernetes插件或者用户应用）能够与kube-apiserver交互，Kubernetes会默认在命名空间下创建一个名为kubernetes的服务，如下所示：

```
$ kubectl get svc kubernetes -o wide
NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE       SELECTOR
kubernetes            ClusterIP   10.96.0.1       <none>        443/TCP          166d      <none>
```
而该kubernetes服务代理的后端实际地址通过endpoints进行维护，如下所示：

```
$ kubectl get endpoints kubernetes
NAME         ENDPOINTS        AGE
kubernetes   192.168.1.4:6443   166d
```
通过这种方式集群内的应用或者系统主机就可以通过集群内部的DNS域名kubernetes.default.svc访问到部署外部的kube-apiserver实例。 

因此，如果我们想要监控kube-apiserver相关的指标，只需要通过endpoints资源找到kubernetes对应的所有后端地址即可。  

如下所示，创建监控任务kubernetes-apiservers，这里指定了服务发现模式为endpoints。Promtheus会查找当前集群中所有的endpoints配置，并通过relabel进行判断是否为apiserver对应的访问地址：


```
  - job_name: 'kubernetes-apiservers'
    scheme: https
    tls_config:
      insecure_skip_verify: true
    bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
    kubernetes_sd_configs:
    - role: endpoints
      api_server: https://192.168.1.4:6443
      bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
      tls_config:
        insecure_skip_verify: true
    relabel_configs:
    - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
      action: keep
      regex: default;kubernetes;https
```
在relabel_configs配置中用于判断当前endpoints是否为kube-apiserver对用的地址。重新加载配置文件，重建Promthues实例，得到以下结果。

#### 监控kube-schedule、kube-control-manager、kube-proxy
在prometheus里手动添加kubernetes-schedule、kubernetes-control-manager组件的连接配置，非证书连接！以下组件的配置，还不需要使用证书连接，直接ip+port就可以，默认路径就是/metrics
确保以下四个组件的metrcis数据可以通过下面方式正常获取。  

schedule的metrics接口 （Scheduler服务端口默认为10251）

```
  - job_name: 'kubernetes-schedule'          #任务名
    scrape_interval: 5s                   #本任务的抓取间隔，覆盖全局配置
    static_configs:
      - targets: ['192.168.1.4:10251']
```

control-manager的metrics接口（ControllerManager服务端口默认为10252）

```
  - job_name: 'kubernetes-control-manager'
    scrape_interval: 5s
    static_configs:
      - targets: ['192.168.1.4:10252']
```

kube-proxy的metrics接口(kube-proxy服务端口默认为10249）

```
  - job_name: 'kubernetes-proxy'
    scrape_interval: 5s
    static_configs:
      - targets: ['192.168.1.4:10249', '192.168.1.5：10249', '192.168.1.6:10249' ]
```

当然，还可用服务发现的方式监控，具体如下：
创建service：

```
apiVersion: v1
kind: Service
metadata:
  namespace: kube-system
  name: kube-scheduler-prometheus-discovery
  labels:
    k8s-app: kube-scheduler
  annotations:
    prometheus.io/scrape: 'true'
spec:
  selector:
    component: kube-scheduler
  type: ClusterIP
  clusterIP: None
  ports:
  - name: http-metrics
    port: 10251
    targetPort: 10251
    protocol: TCP
	
---

apiVersion: v1
kind: Service
metadata:
  namespace: kube-system
  name: kube-controller-manager-prometheus-discovery
  labels:
    k8s-app: kube-controller-manager
  annotations:
    prometheus.io/scrape: 'true'
spec:
  selector:
    component: kube-controller-manager
  type: ClusterIP
  clusterIP: None
  ports:
  - name: http-metrics
    port: 10252
    targetPort: 10252
    protocol: TCP
	
---

apiVersion: v1
kind: Service
metadata:
  namespace: kube-system
  name: kube-proxy-prometheus-discovery
  labels:
    k8s-app: kube-proxy
  annotations:
    prometheus.io/scrape: 'true'
spec:
  selector:
    k8s-app: kube-proxy
  type: NodePort
  ports:
  - name: http-metrics
    port: 10249
    targetPort: 10249
    nodePort: 30025
    protocol: TCP
```

创建监控任务：

```
  - job_name: 'kube-scheduler-prometheus-discovery'
    kubernetes_sd_configs:
    - role: endpoints
      api_server: https://192.168.1.4:6443
      tls_config:
        insecure_skip_verify: true
      bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
    relabel_configs:
        # 选择哪些label
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape, __meta_kubernetes_namespace, __meta_kubernetes_service_name]
          # 上述选择的label的值需要与下述对应
      regex: true;kube-system;kube-scheduler-prometheus-discovery
          # 含有符合regex的source_label的endpoints进行保留
      action: keep
  - job_name: 'kube-controller-manager-discovery'
    kubernetes_sd_configs:
    - role: endpoints
      api_server: https://192.168.1.4:6443
      tls_config:
        insecure_skip_verify: true
      bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
    relabel_configs:
        # 选择哪些label
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape, __meta_kubernetes_namespace, __meta_kubernetes_service_name]
          # 上述选择的label的值需要与下述对应
      regex: true;kube-system;kube-controller-manager-prometheus-discovery
          # 含有符合regex的source_label的endpoints进行保留
      action: keep
  - job_name: 'kube-proxy-prometheus-discovery'
    kubernetes_sd_configs:
    - role: endpoints
      api_server: https://192.168.1.4:6443
      tls_config:
        insecure_skip_verify: true
      bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
    relabel_configs:
        # 选择哪些label
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape, __meta_kubernetes_namespace, __meta_kubernetes_service_name]
          # 上述选择的label的值需要与下述对应
      regex: true;kube-system;kube-proxy-prometheus-discovery
          # 含有符合regex的source_label的endpoints进行保留
      action: keep

```



#### 从Kubelet获取节点运行状态
Kubelet组件运行在Kubernetes集群的各个节点中，其负责维护和管理节点上Pod的运行状态。kubelet组件的正常运行直接关系到该节点是否能够正常的被Kubernetes集群正常使用。

基于Node模式，Prometheus会自动发现Kubernetes中所有Node节点的信息并作为监控的目标Target。 而这些Target的访问地址实际上就是Kubelet的访问地址，并且Kubelet实际上直接内置了对Promtheus的支持。

实际探索过程中，直接从kuberlet获取数据有报错。这里采用第二种方式：不直接通过kubelet的metrics服务采集监控数据，而通过Kubernetes的api-server提供的代理API访问各个节点中kubelet的metrics服务，如下所示：

修改prometheus.yml配置文件，并添加以下采集任务配置：

```
  - job_name: 'kubernetes-kubelet'
    scheme: https
    tls_config:
      insecure_skip_verify: true
    bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
    kubernetes_sd_configs:
    - role: node
      api_server: https://192.168.1.4:6443
      bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
      tls_config:
        insecure_skip_verify: true
    relabel_configs:
    - action: labelmap
      regex: __meta_kubernetes_node_label_(.+)
    - target_label: __address__
      replacement: 192.168.1.4:6443
    - source_labels: [__meta_kubernetes_node_name]
      regex: (.+)
      target_label: __metrics_path__
      replacement: /api/v1/nodes/${1}/proxy/metrics
```
通过relabeling，将从Kubernetes获取到的默认地址__address__替换为192.168.1.4:6443。同时将__metrics_path__替换为api-server的代理地址/api/v1/nodes/${1}/proxy/metrics。

#### 监控kube-dns
kube-dns会在9153端口暴露采集指标，通过服务发现可以实现对kube-dns的监控

```
  - job_name: 'kube-dns-discovery'
    tls_config:
      insecure_skip_verify: true
    bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
    scheme: https
    kubernetes_sd_configs:
    - role: endpoints
      api_server: https://192.168.1.4:6443
      tls_config:
        insecure_skip_verify: true
      bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
    relabel_configs:
    - source_labels: [__meta_kubernetes_endpoint_port_name]
      separator: ;
      regex: metrics
      replacement: $1
      action: keep
    - source_labels: [__address__]
      action: replace
      target_label: instance
    - target_label: __address__
      replacement: 192.168.1.4:6443
    - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_pod_name, __meta_kubernetes_pod_container_port_number]
      regex: ([^;]+);([^;]+);([^;]+)
      target_label: __metrics_path__
      replacement: /api/v1/namespaces/${1}/pods/${2}:${3}/proxy/metrics
        # 选择哪些label
    - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name]
          # 上述选择的label的值需要与下述对应
      regex: kube-system;kube-dns
          # 含有符合regex的source_label的endpoints进行保留
      action: keep
```

#### 从cadvisor获取容器的监控数据
cAdvisor可以对节点机器上的资源及容器进行实时监控和性能数据采集，包括CPU使用情况、内存使用情况、网络吞吐量及文件系统使用情况。Kubernetes内置对cAdvisor支持。外部的Prometheus可以通过Api Server的代理访问到cAdvisor：

```
  - job_name: 'kubernetes-cadvisor'
    scheme: https
    tls_config:
      insecure_skip_verify: true
    bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
    kubernetes_sd_configs:
    - role: node
      api_server: https://192.168.1.4:6443
      bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
      tls_config:
        insecure_skip_verify: true
    relabel_configs:
    - target_label: __address__
      replacement: 192.168.1.4:6443
    - source_labels: [__meta_kubernetes_node_name]
      regex: (.+)
      target_label: __metrics_path__
      replacement: /api/v1/nodes/${1}/proxy/metrics/cadvisor
    - action: labelmap
      regex: __meta_kubernetes_node_label_(.+)
```

#### 使用NodeExporter监控集群资源使用情况
为了能够采集集群中各个节点的资源使用情况，我们需要在各节点中部署一个Node Exporter实例。在本章的“部署Prometheus”小节，我们使用了Kubernetes内置的控制器之一Deployment。Deployment能够确保Prometheus的Pod能够按照预期的状态在集群中运行，而Pod实例可能随机运行在任意节点上。而与Prometheus的部署不同的是，对于Node Exporter而言每个节点只需要运行一个唯一的实例，此时，就需要使用Kubernetes的另外一种控制器Daemonset。顾名思义，Daemonset的管理方式类似于操作系统中的守护进程。Daemonset会确保在集群中所有（也可以指定）节点上运行一个唯一的Pod实例。

创建node-exporter-daemonset.yml文件，并写入以下内容：

```
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
spec:
  selector:
    matchLabels:
      app: node-exporter
  template:
    metadata:
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '9100'
        prometheus.io/path: 'metrics'
      labels:
        app: node-exporter
      name: node-exporter
    spec:
      tolerations:
      - key: "node-role.kubernetes.io/master"
        operator: "Equal"
        effect: "NoSchedule"
      containers:
      - image: prom/node-exporter
        imagePullPolicy: IfNotPresent
        name: node-exporter
        ports:
        - containerPort: 9100
          hostPort: 9100
          name: scrape
      hostNetwork: true
      hostPID: true
```
由于Node Exporter需要能够访问宿主机，因此这里指定了hostNetwork和hostPID，让Pod实例能够以主机网络以及系统进程的形式运行。同时YAML文件中也创建了NodeExporter相应的Service。这样通过Service就可以访问到对应的NodeExporter实例。


```
$ kubectl create -f node-exporter-daemonset.yml
service "node-exporter" created
daemonset "node-exporter" created
```

目前为止，通过Daemonset的形式将Node Exporter部署到了集群中的各个节点中。接下来，我们只需要通过Prometheus的pod服务发现模式，找到当前集群中部署的Node Exporter实例即可。 需要注意的是，由于Kubernetes中并非所有的Pod都提供了对Prometheus的支持，有些可能只是一些简单的用户应用，为了区分哪些Pod实例是可以供Prometheus进行采集的，这里我们为Node Exporter添加了注解：

```
prometheus.io/scrape: 'true'
```

由于Kubernetes中Pod可能会包含多个容器，还需要用户通过注解指定用户提供监控指标的采集端口：

```
prometheus.io/port: '9100'
```

而有些情况下，Pod中的容器可能并没有使用默认的/metrics作为监控采集路径，因此还需要支持用户指定采集路径：

```
prometheus.io/path: 'metrics'
```
为Prometheus创建监控采集任务kubernetes-nodes，如下所示：

```
 - job_name: 'kubernetes-nodes'
    kubernetes_sd_configs:
    - role: pod
      api_server: https://192.168.1.4:6443
      bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
      tls_config:
        insecure_skip_verify: true
    relabel_configs:
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
      action: keep
      regex: true
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
      action: replace
      target_label: __metrics_path__
      regex: (.+)
    - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
      action: replace
      regex: ([^:]+)(?::\d+)?;(\d+)
      replacement: $1:$2
      target_label: __address__
    - action: labelmap
      regex: __meta_kubernetes_pod_label_(.+)
    - source_labels: [__meta_kubernetes_namespace]
      action: replace
      target_label: kubernetes_namespace
    - source_labels: [__meta_kubernetes_pod_name]
      action: replace
      target_label: kubernetes_pod_name
    - source_labels:  ["__mkubernetes_pod_node_name"]
      target_label: "node_name"
```
#### 使用kube-state-metrics监控资源对象

通过kube-state-metrics可以获取以下指标
- CronJob Metrics
- DaemonSet Metrics
- Deployment Metrics
- Job Metrics
- LimitRange Metrics
- Node Metrics
- PersistentVolume Metrics
- PersistentVolumeClaim Metrics
- Pod Metrics
- ReplicaSet Metrics
- ReplicationController Metrics
- ResourceQuota Metrics
- Service Metrics
- StatefulSet Metrics
- Namespace Metrics
- Horizontal Pod Autoscaler Metrics
- Endpoint Metrics

##### Kubernetes版本支持
kube-state-metrics用于client-go与Kubernetes集群通信。支持的Kubernetes集群版本由决定client-go。可以在此处找到client-go和Kubernetes集群的兼容性矩阵 。
| kube-state-metrics | **Kubernetes 1.12** | **Kubernetes 1.13** | **Kubernetes 1.14** |  **Kubernetes 1.15** |  **Kubernetes 1.16** | **Kubernetes 1.17** |
|--------------------|---------------------|---------------------|---------------------|----------------------|----------------------|----------------------|
| **v1.5.0**         |         ✓           |         -           |         -           |          -           |          -           | - |
| **v1.6.0**         |         ✓           |         ✓           |         -           |          -           |          -           | - |
| **v1.7.2**         |         ✓           |         ✓           |         ✓           |          -           |          -           | - |
| **v1.8.0**         |         ✓           |         ✓           |         ✓           |          ✓           |          -           | - |
| **v1.9.4**         |         ✓           |         ✓           |         ✓           |          ✓           |          ✓           |  -| 
| **master**         |         ✓           |         ✓           |         ✓           |          ✓           |          ✓           | ✓           |          ✓           |


##### 部署kube-state-metrics

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    app.kubernetes.io/name: kube-state-metrics
    app.kubernetes.io/version: v1.9.4
  name: kube-state-metrics
rules:
- apiGroups:
  - ""
  resources:
  - configmaps
  - secrets
  - nodes
  - nodes/proxy
  - pods
  - pods/proxy
  - services/proxy
  - services
  - resourcequotas
  - replicationcontrollers
  - limitranges
  - persistentvolumeclaims
  - persistentvolumes
  - namespaces
  - endpoints
  verbs:
  - list
  - watch
  - get
- apiGroups:
  - extensions
  resources:
  - daemonsets
  - deployments
  - replicasets
  - ingresses
  verbs:
  - list
  - watch
- apiGroups:
  - apps
  resources:
  - statefulsets
  - daemonsets
  - deployments
  - replicasets
  verbs:
  - list
  - watch
- apiGroups:
  - batch
  resources:
  - cronjobs
  - jobs
  verbs:
  - list
  - watch
- apiGroups:
  - autoscaling
  resources:
  - horizontalpodautoscalers
  verbs:
  - list
  - watch
- apiGroups:
  - authentication.k8s.io
  resources:
  - tokenreviews
  verbs:
  - create
- apiGroups:
  - authorization.k8s.io
  resources:
  - subjectaccessreviews
  verbs:
  - create
- apiGroups:
  - policy
  resources:
  - poddisruptionbudgets
  verbs:
  - list
  - watch
- apiGroups:
  - certificates.k8s.io
  resources:
  - certificatesigningrequests
  verbs:
  - list
  - watch
- apiGroups:
  - storage.k8s.io
  resources:
  - storageclasses
  - volumeattachments
  verbs:
  - list
  - watch
- apiGroups:
  - admissionregistration.k8s.io
  resources:
  - mutatingwebhookconfigurations
  - validatingwebhookconfigurations
  verbs:
  - list
  - watch
- apiGroups:
  - networking.k8s.io
  resources:
  - networkpolicies
  verbs:
  - list
  - watch

---

apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    app.kubernetes.io/name: kube-state-metrics
    app.kubernetes.io/version: v1.9.4
  name: kube-state-metrics
  namespace: kube-system
  
---

apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  labels:
    app.kubernetes.io/name: kube-state-metrics
    app.kubernetes.io/version: v1.9.4
  name: kube-state-metrics
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: kube-state-metrics
subjects:
- kind: ServiceAccount
  name: kube-state-metrics
  namespace: kube-system

---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app.kubernetes.io/name: kube-state-metrics
    app.kubernetes.io/version: v1.9.4
  name: kube-state-metrics
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: kube-state-metrics
  template:
    metadata:
      labels:
        app.kubernetes.io/name: kube-state-metrics
        app.kubernetes.io/version: v1.9.4
    spec:
      containers:
      - image: quay.io/coreos/kube-state-metrics:v1.9.4
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 5
          timeoutSeconds: 5
        name: kube-state-metrics
        ports:
        - containerPort: 8080
          name: http-metrics
        - containerPort: 8081
          name: telemetry
        readinessProbe:
          httpGet:
            path: /
            port: 8081
          initialDelaySeconds: 5
          timeoutSeconds: 5
      nodeSelector:
        kubernetes.io/os: linux
      serviceAccountName: kube-state-metrics

---
apiVersion: v1
kind: Service
metadata:
  labels:
    app.kubernetes.io/name: kube-state-metrics
    app.kubernetes.io/version: v1.9.4
  name: kube-state-metrics
  namespace: kube-system
spec:
  clusterIP: None
  ports:
  - name: http-metrics
    port: 8080
    targetPort: http-metrics
  - name: telemetry
    port: 8081
    targetPort: telemetry
  selector:
    app.kubernetes.io/name: kube-state-metrics

```

##### prometheus创建kube-state-netrics监控任务

通过kubernetes服务发现，监控kube-state-metrics
```
  - job_name: 'kubernetes-kube-state-metrics'
    tls_config:
      insecure_skip_verify: true
    bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
    scheme: https
    kubernetes_sd_configs:
    - role: endpoints
      api_server: https://192.168.1.4:6443
      tls_config:
        insecure_skip_verify: true
      bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
    relabel_configs:
    - source_labels: [ __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
      action: keep
      regex: kube-state-metrics;http-metrics
    - source_labels: [__address__]
      action: replace
      target_label: instance
    - target_label: __address__
      replacement: 192.168.1.4:6443
    - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_pod_name, __meta_kubernetes_pod_container_port_number]
      regex: ([^;]+);([^;]+);([^;]+)
      target_label: __metrics_path__
      replacement: /api/v1/namespaces/${1}/pods/http:${2}:${3}/proxy/metrics
    - action: labelmap
      regex: __meta_kubernetes_service_label_(.+)
    - source_labels: [__meta_kubernetes_namespace]
      action: replace
      target_label: kubernetes_namespace
    - source_labels: [__meta_kubernetes_service_name]
      action: replace
      target_label: kubernetes_name
```

#### 内置对prometheus支持的应用监控

对于内置了Promthues支持的应用，需要从Pod实例中采集其自定义监控指标。在这需要对应用添加以annotations：
- prometheus.io/scrape: 'true'
- prometheus.io/port: 'your_port'
- prometheus.io/path: 'your_metrics_path'

通过这些标签可以筛选掉无用的应用。

添加promtheus任务

```
  - job_name: 'kubernetes-kube-service'
    tls_config:
      insecure_skip_verify: true
    bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
    scheme: https
    kubernetes_sd_configs:
    - role: endpoints
      api_server: https://192.168.1.4:6443
      tls_config:
        insecure_skip_verify: true
      bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
    relabel_configs:
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
      action: keep
      regex: true
    - source_labels: [__address__]
      action: replace
      target_label: instance
    - target_label: __address__
      replacement: 192.168.1.4:6443
    - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_pod_name, __meta_kubernetes_pod_container_port_number, __meta_kubernetes_service_annotation_prometheus_io_path]
      regex: ([^;]+);([^;]+);([^;]+);([^;]+)
      target_label: __metrics_path__
      replacement: /api/v1/namespaces/${1}/pods/http:${2}:${3}/proxy/${4}
    - action: labelmap
      regex: __meta_kubernetes_service_label_(.+)
    - source_labels: [__meta_kubernetes_namespace]
      action: replace
      target_label: kubernetes_namespace
    - source_labels: [__meta_kubernetes_service_name]
      action: replace
      target_label: kubernetes_name
```

#### 对Ingress和Service进行网络探测
为了能够对Ingress和Service进行探测，我们需要在集群部署Blackbox Exporter实例。 如下所示，创建blackbox-exporter.yaml用于描述部署相关的内容

```
apiVersion: v1
kind: Service
metadata:
  labels:
    app: blackbox-exporter
  name: blackbox-exporter
spec:
  ports:
  - name: blackbox
    port: 9115
    protocol: TCP
  selector:
    app: blackbox-exporter
  type: ClusterIP
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: blackbox-exporter
  name: blackbox-exporter
spec:
  replicas: 1
  selector:
    matchLabels:
      app: blackbox-exporter
  template:
    metadata:
      labels:
        app: blackbox-exporter
    spec:
      containers:
      - image: prom/blackbox-exporter
        imagePullPolicy: IfNotPresent
        name: blackbox-exporter
```

为了能够让Prometheus能够自动的对Service进行探测，我们需要通过服务发现自动找到所有的Service信息。 如下所示，在Prometheus的配置文件中添加名为kubernetes-services的监控采集任务：

```
  - job_name: 'kubernetes-services'
    tls_config:
      insecure_skip_verify: true
    bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
    scheme: https
    params:
      module: [http_2xx]
    kubernetes_sd_configs:
    - role: service
      api_server: https://192.168.1.4:6443
      tls_config:
        insecure_skip_verify: true
      bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
    relabel_configs:
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_probe]
      action: keep
      regex: true
    - source_labels: [__address__]
      target_label: __param_target
    - target_label: __address__
      replacement: 192.168.1.4:6443
    - target_label: __metrics_path__
      replacement: api/v1/namespaces/default/services/blackbox-exporter:9115/proxy/probe
    - source_labels: [__param_target]
      target_label: instance
    - action: labelmap
      regex: __meta_kubernetes_service_label_(.+)
    - source_labels: [__meta_kubernetes_namespace]
      target_label: kubernetes_namespace
    - source_labels: [__meta_kubernetes_service_name]
      target_label: kubernetes_name
```

在该任务配置中，通过指定kubernetes_sd_config的role为service指定服务发现模式：

```
kubernetes_sd_configs:
    - role: service
      api_server: https://192.168.1.4:6443
      tls_config:
        insecure_skip_verify: true
      bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
```

为了区分集群中需要进行探测的Service实例，我们通过标签‘prometheus.io/probe: true’进行判断，从而过滤出需要探测的所有Service实例：

```
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_probe]
      action: keep
      regex: true
```

为了能够在外部访问k8s集群内部的blackbox，这里使用的Kubernetes proxy api

```
    - target_label: __address__
      replacement: 192.168.1.4:6443
    - target_label: __metrics_path__
      replacement: api/v1/namespaces/default/services/blackbox-exporter:9115/proxy/probe
```

对于Ingress而言，也是一个相对类似的过程，这里给出对Ingress探测的Promthues任务配置作为参考：

```
  - job_name: 'kubernetes-ingresses'
    tls_config:
      insecure_skip_verify: true
    bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
    scheme: https
    params:
      module: [http_2xx]
    kubernetes_sd_configs:
    - role: ingress
      api_server: https://192.168.1.4:6443
      tls_config:
        insecure_skip_verify: true
      bearer_token_file: C:/Users/Administrator/Desktop/prometheus-token
    relabel_configs:
    - source_labels: [__meta_kubernetes_ingress_annotation_prometheus_io_probe]
      action: keep
      regex: true
    - source_labels: [__meta_kubernetes_ingress_scheme,__address__,__meta_kubernetes_ingress_path]
      regex: (.+);(.+);(.+)
      replacement: ${1}://${2}${3}
      target_label: __param_target
    - target_label: __address__
      replacement: 192.168.1.4:6443
    - target_label: __metrics_path__
      replacement: api/v1/namespaces/default/services/blackbox-exporter:9115/proxy/probe
    - source_labels: [__param_target]
      target_label: instance
    - action: labelmap
      regex: __meta_kubernetes_ingress_label_(.+)
    - source_labels: [__meta_kubernetes_namespace]
      target_label: kubernetes_namespace
    - source_labels: [__meta_kubernetes_ingress_name]
      target_label: kubernetes_name
```

### prometheus部署在k8s集群内部监控实现
prometheus部署在k8s集群内部监控k8s和部署在外部监控的原理是一样的，唯一的区别：
- 集群内部，可以通过集群的DNS访问监控对象，不需要通过api server代理。
- 服务发现时，不需要制定api server 的地址。 

具体过程如下：

1.授权

```
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRole
metadata:
  name: prometheus
rules:
- apiGroups: [""]
  resources:
  - nodes
  - nodes/proxy
  - pods
  - proxy
  - pods/proxy
  - services
  - services/proxy
  - endpoints
  - pods
  verbs: ["get", "list", "watch"]
- apiGroups:
  - extensions
  resources:
  - ingresses
  verbs: ["get", "list", "watch"]
- nonResourceURLs: ["/metrics"]
  verbs: ["get"]
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: prometheus
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: prometheus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: prometheus
subjects:
- kind: ServiceAccount
  name: prometheus
  namespace: default
```

2.将prometheus的配置放在configmap中

```
apiVersion: v1
data:
  prometheus.yml: |-
    global:
      scrape_interval:     15s 
      evaluation_interval: 15s
    scrape_configs:
    - job_name: 'kubernetes-apiservers'
      kubernetes_sd_configs:
      - role: endpoints
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      relabel_configs:
      - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: default;kubernetes;https
      - target_label: __address__
        replacement: kubernetes.default.svc:443
    - job_name: 'kube-scheduler'
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      kubernetes_sd_configs:
      - role: endpoints
      relabel_configs:
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape, __meta_kubernetes_namespace, __meta_kubernetes_service_name]
        regex: true;kube-system;kube-scheduler-prometheus-discovery
        action: keep
    - job_name: 'kube-controller-manager'
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      kubernetes_sd_configs:
      - role: endpoints
      relabel_configs:
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape, __meta_kubernetes_namespace, __meta_kubernetes_service_name]
        regex: true;kube-system;kube-controller-manager-prometheus-discovery
        action: keep
    - job_name: 'kubernetes-kubelet'
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      kubernetes_sd_configs:
      - role: node
      relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
      - target_label: __address__
        replacement: kubernetes.default.svc:443
      - source_labels: [__meta_kubernetes_node_name]
        regex: (.+)
        target_label: __metrics_path__
        replacement: /api/v1/nodes/${1}/proxy/metrics
      - source_labels: [__meta_kubernetes_node_name]
        target_label: "kubernetes_node_name"
    - job_name: 'kubernetes-cadvisor'
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      kubernetes_sd_configs:
      - role: node
      relabel_configs:
      - target_label: __address__
        replacement: kubernetes.default.svc:443
      - source_labels: [__meta_kubernetes_node_name]
        regex: (.+)
        target_label: __metrics_path__
        replacement: /api/v1/nodes/${1}/proxy/metrics/cadvisor
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
    - job_name: 'kube-proxy'
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      kubernetes_sd_configs:
      - role: endpoints
      relabel_configs:
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape, __meta_kubernetes_namespace, __meta_kubernetes_service_name]
        regex: true;kube-system;kube-proxy-prometheus-discovery
        action: keep
    - job_name: 'kube-dns-discovery'
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      kubernetes_sd_configs:
      - role: endpoints
      relabel_configs:
      - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name]
        regex: kube-system;kube-dns
        action: keep
      - source_labels: [__meta_kubernetes_endpoint_port_name]
        separator: ;
        regex: metrics
        replacement: $1
        action: keep
      - source_labels: [__address__]
        action: replace
        target_label: instance
    - job_name: 'kube-state-metrics'        
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      kubernetes_sd_configs:
      - role: endpoints
      relabel_configs:
      - source_labels: [__meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        regex: kube-state-metrics;http-metrics
        action: keep
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scheme]
        action: replace
        target_label: __scheme__
        regex: (https?)
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_service_annotation_prometheus_io_port]
        action: replace
        target_label: __address__
        regex: (.+)(?::\d+);(\d+)
        replacement: $1:$2
      - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_service_name]
        action: replace
        target_label: kubernetes_name        
    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: kubernetes_pod_name   
      - source_labels: [__meta_kubernetes_pod_node_name]
        target_label: kubernetes_node_name   
    - job_name: 'kubernetes-services'
      metrics_path: /probe
      params:
        module: [http_2xx]
      kubernetes_sd_configs:
      - role: service
      relabel_configs:
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_probe]
        action: keep
        regex: true
      - source_labels: [__address__]
        target_label: __param_target
      - target_label: __address__
        replacement: blackbox-exporter.default.svc.cluster.local:9115
      - source_labels: [__param_target]
        target_label: instance
      - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_service_name]
        target_label: kubernetes_name
    - job_name: 'kubernetes-ingresses'
      metrics_path: /probe
      params:
        module: [http_2xx]
      kubernetes_sd_configs:
      - role: ingress
      relabel_configs:
      - source_labels: [__meta_kubernetes_ingress_annotation_prometheus_io_probe]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_ingress_scheme,__address__,__meta_kubernetes_ingress_path]
        regex: (.+);(.+);(.+)
        replacement: ${1}://${2}${3}
        target_label: __param_target
      - target_label: __address__
        replacement: blackbox-exporter.default.svc.cluster.local:9115
      - source_labels: [__param_target]
        target_label: instance
      - action: labelmap
        regex: __meta_kubernetes_ingress_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_ingress_name]
        target_label: kubernetes_name


kind: ConfigMap
metadata:
  name: prometheus-config

```

3.创建prometheus service和deployment

```
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    name: prometheus
  name: prometheus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      serviceAccountName: prometheus
      serviceAccount: prometheus
      containers:
      - name: prometheus
        image: prom/prometheus:v2.2.1
        command:
        - "/bin/prometheus"
        args:
        - "--config.file=/etc/prometheus/prometheus.yml"
        - "--web.enable-lifecycle"
        ports:
        - containerPort: 9090
          protocol: TCP
        volumeMounts:
        - mountPath: "/etc/prometheus"
          name: prometheus-config
      volumes:
      - name: prometheus-config
        configMap:
          name: prometheus-config
        
---

apiVersion: v1
kind: "Service"
metadata:
  name: prometheus
  labels:
    name: prometheus
spec:
  ports:
  - name: prometheus
    protocol: TCP
    port: 9090
    targetPort: 9090
    nodePort: 30090
  selector:
    app: prometheus
  type: NodePort

```

这里创建的prometheus service是NodePort类型，可以直接通过ip:30090访问prometheus。

## kubernetes监控方案
上面讲述了如何在集群外部和集群内部监控k8s 。对于单集群来说，这两种方案已经能够满足我们的需求。那对于多集群监控呢。下面列出两种方案：

方案 | 优势 | 劣势
---|---|---
采用外部部署prometheus的方式，写多套配置 | 无需对k8s造成额外的资源占用 | 增加了api server的负载
利用联邦集群，每个k8s中部署一个prometheus，由外部prometheus汇总 | api server负载小|对k8s造成额外的资源占用

两种方案各有各自的优缺点，在部署实施过程中，可根据需求选择对应方案。

