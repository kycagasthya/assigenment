package test

import (
	"testing"
	"io/ioutil"
	"log"
	"encoding/json"
	"github.com/go-playground/validator"
	"github.com/stretchr/testify/assert"
)

type Config struct {
	ClientID	string		`json:"client_id" validate:"required"`
	DatasetID	string		`json:"dataset_id" validate:"required"`
	Sources		struct {}	`json:"sources" validate:"required"`
	Tables		struct {}	`json:"tables" validate:"required"`
}

var validate *validator.Validate

func TestValidateTFVars(t *testing.T) {
	validate = validator.New()

	yml, err := ioutil.ReadFile("../../terraform/datalake/terraform.auto.tfvars.json")
	if err != nil {
		log.Fatal(err)
	}

	cfg := Config{}
	err = json.Unmarshal(yml, &cfg)
	if err != nil {
		log.Fatal(err)
	}

	err = validate.Struct(cfg)
	assert.NoError(t, err)
	assert.Equal(t, cfg.ClientID, "acme")
	assert.Equal(t, cfg.DatasetID, "datalake_acme")
}
