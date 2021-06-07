# kubeflow-tutorial

## 설치 환경

- Windows 10 WSL2
    - Ubuntu : 20.04 LTS
    - Docker : v20.10.6
    - kuberenetes, kubectl : v1.19.7
    - Kubeflow : kfctl_istio_dex.v1.2.0.yaml
    - kfctl: v1.2.0-0-gbc038f9

- 단일 사용자가 로컬에서만 사용할 경우 : [kfctl_k8s_istio](https://v1-2-branch.kubeflow.org/docs/started/k8s/kfctl-k8s-istio/)
- 여러 사용자가 사용해야 해서 인증이 필요한 경우 : [kfctl_istio_dex](https://v1-2-branch.kubeflow.org/docs/started/k8s/kfctl-istio-dex/)

## (istio_dex를 사용할 경우) kubernetes 설정 수정

Kubeflow를 설치하기 위해서는 kubernetes API server를 수정해야 하는데, Docker Desktop을 통해 kubernetes를 사용하고 있기 때문에 설정 파일이 로컬에 존재하지 않는다. 

```bash
$ cat /etc/kubernetes/manifests/kube-apiserver.yaml
cat: /etc/kubernetes/manifests/kube-apiserver.yaml: No such file or directory
```

따라서, 다음 방법을 이용하여 API server를 수정한다.

```bash
# Edit kube-apiserver.yaml in docker-desktop
# docker run -it --privileged --pid=host debian nsenter -t 1 -m -u -n -i sh
# vi /var/lib/kubeadm/manifests/kube-apiserver.yaml
# ADD FOLLLOWING: spec.containers.command
        # - --service-account-signing-key-file=/run/config/pki/sa.key
        # - --service-account-issuer=kubernetes.default.svc
        # - --feature-gates=TokenRequest=true
        # - --feature-gates=TokenRequestProjection=true
```

`sa.key` 파일이 해당 위치에 없을 수도 있으므로 `/etc/kubernetes/pki/sa.key` 등에 있다면 해당 경로에 맞춰 내용을 수정한다.

## kfctl 설치

```bash
wget https://github.com/kubeflow/kfctl/releases/download/v1.2.0/kfctl_v1.2.0-0-gbc038f9_linux.tar.gz
tar -xvf kfctl_v1.2.0-0-gbc038f9_linux.tar.gz
sudo mv kfctl /usr/local/bin/
rm kfctl_v1.2.0-0-gbc038f9_linux.tar.gz
kfctl version # kfctl_v1.2.0-0-gbc038f9
```

`/usr/local/bin` 으로 이동하지 않을 경우 `$PATH`에 추가해서 사용할 수도 있다.

## Kubeflow 설치

- k8s_istio

```bash
wget https://raw.githubusercontent.com/kubeflow/manifests/v1.2-branch/kfdef/kfctl_k8s_istio.v1.2.0.yaml
kfctl apply -f kfctl_k8s_istio.v1.2.0.yaml -V
```

- istio_dex

```bash
wget https://raw.githubusercontent.com/kubeflow/manifests/v1.2-branch/kfdef/kfctl_istio_dex.v1.2.0.yaml
kfctl apply -f kfctl_istio_dex.v1.2.0.yaml -V
```

설치가 완료되면 port-forward 명령어로 8080 포트로 접속할 수 있도록 한다.

```bash
kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80
```

istio_dex의 경우 초기 아이디와 비밀번호는 `admin@kubeflow.org / 12341234` 이다. 유저를 추가하는 방법에 대해서는 [document](https://v1-2-branch.kubeflow.org/docs/started/k8s/kfctl-istio-dex/#add-static-users-for-basic-auth)에 나와있다.

[localhost:8080](http://localhost:8080) 으로 접속하여 Kubeflow Dashboard에 접속했다면 설치 완료!

설치 완료 후 초기 컨테이너 image를 pull하고 running 하느라 시간이 다소 걸릴 수 있다. `kubectl get pods -n kubeflow` 에서 모든 pods 가 생성되어 동작할 때 까지 기다린다.
