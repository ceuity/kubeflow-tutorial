import kfp
from kfp import dsl

BASE_IMAGE = "library/bash:4.4.23"
KUBEFLOW_HOST = "http://localhost:8080/pipeline"


def echo_op():
    return dsl.ContainerOp(
        name="echo",
        image=BASE_IMAGE,
        command=["sh", "-c"],
        arguments=['echo "Hello World!"'],
    )


@dsl.pipeline(name="hello_world_bash_pipeline", description="A Hello World Pipeline")
def hello_world_bash_pipeline():
    echo_task = echo_op()


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(hello_world_bash_pipeline, __file__ + ".zip")
    kfp.Client(host=KUBEFLOW_HOST).create_run_from_pipeline_func(
        hello_world_bash_pipeline,
        arguments={},
        experiment_name="hello-world-bash-experiment",
    )
