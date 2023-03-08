package test

import (
	"fmt"
	"os"
	"testing"

	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestTerraformAcme(t *testing.T) {
	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../../terraform/datalake",
		VarFiles:     []string{"terraform.auto.tfvars.json"},
		BackendConfig: map[string]interface{}{
			"bucket": fmt.Sprintf("%s-state", os.Getenv("TF_VAR_project")),
		},
		Reconfigure: true,
	})

	defer terraform.Destroy(t, terraformOptions)

	terraform.InitAndApply(t, terraformOptions)

	outSubscrList := terraform.Output(t, terraformOptions, "subscr_list")
	outTableList := terraform.Output(t, terraformOptions, "table_list")

	subscriptionsList := "acme-t_locations-v1"
	subscriptionsList = subscriptionsList + ",acme-t_products-v1"

	tableList := fmt.Sprintf("%[1]s:datalake_acme.acme_locations_table", os.Getenv("TF_VAR_project"))
	tableList = tableList + fmt.Sprintf(",%[1]s:datalake_acme.acme_products_table", os.Getenv("TF_VAR_project"))

	assert.Equal(t, subscriptionsList, outSubscrList, "Subs lists should be the same.")
	assert.Equal(t, tableList, outTableList, "Table lists should be the same.")
}
