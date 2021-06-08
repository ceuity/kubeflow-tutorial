import kfp

EXPERIMENT_NAME = "Add Number Pipeline"
BASE_IMAGE = "python:3.7"
KUBEFLOW_HOST = "http://localhost:8080/pipeline"


@kfp.dsl.python_component(
    name="add_op", description="adds two numbers", base_image=BASE_IMAGE
)
def add(a: float, b: float) -> float:
    "Calculates sum of two arguments"
    print(f"{a} + {b} = {a + b}")
    return a + b


add_op = kfp.components.func_to_container_op(add, base_image=BASE_IMAGE)


@kfp.dsl.pipeline(
    name="Calculation pipeline",
    description="A toy pipeline that performs arithmetic calculations",
)
def calc_pipeline(a: float = 0, b: float = 7):
    add_task = add_op(a, 4)
    add_2_task = add_op(a, b)
    add_3_task = add_op(add_task.output, add_2_task.output)


if __name__ == "__main__":
    arguments = {"a": "7", "b": "8"}
    kfp.Client(host=KUBEFLOW_HOST).create_run_from_pipeline_func(
        calc_pipeline, arguments=arguments, experiment_name=EXPERIMENT_NAME,
    )
