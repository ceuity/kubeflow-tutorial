import kfp

KUBEFLOW_HOST = "http://localhost:8080/pipeline"


def hello_world_component():
    ret = "Hello World!"
    print(ret)
    return ret


@kfp.dsl.pipeline(name="hello_pipeline", description="Hello World Pipeline!")
def hello_world_pipeline():
    hello_world_op = kfp.components.func_to_container_op(hello_world_component)
    _ = hello_world_op()


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(hello_world_pipeline, "hello-world-pipeline.zip")
    kfp.Client(host=KUBEFLOW_HOST, namespace="anonymous").create_run_from_pipeline_func(
        hello_world_pipeline, arguments={}, experiment_name="hello-world-experiment"
    )
