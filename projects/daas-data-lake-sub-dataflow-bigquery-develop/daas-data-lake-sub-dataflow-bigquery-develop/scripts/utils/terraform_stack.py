from python_terraform import Terraform, IsFlagged, IsNotFlagged


class TerraformStack:
    def __init__(self, working_dir: str, project: str, variables: dict):
        self.working_dir = working_dir
        self.project = project
        self.variables = variables

    def init(self, prefix):
        tf = Terraform(
            working_dir=self.working_dir
        )
        backend_config = {
            "bucket": f"{self.project}-state",
            "prefix": prefix
        }
        tf.init(
            capture_output=False, backend_config=backend_config)

    def workspace(self, name):
        tf = Terraform(
            working_dir=self.working_dir
        )

        tf.create_workspace(name)
        tf.set_workspace(name)

    def apply(self, tfargs: dict = {}):
        tf = Terraform(
            working_dir=self.working_dir,
            variables=self.variables
        )
        tf.apply(
            skip_plan=True, capture_output=False, **tfargs)

    def destroy(self):
        tf = Terraform(
            working_dir=self.working_dir,
            variables=self.variables
        )

        tf.destroy(capture_output=False, input=False,
                   no_color=IsFlagged, force=IsNotFlagged, auto_approve=True)
