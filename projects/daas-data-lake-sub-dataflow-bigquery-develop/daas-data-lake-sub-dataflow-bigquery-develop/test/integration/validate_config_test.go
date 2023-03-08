package test

import (
	"testing"
	"io/ioutil"
	"log"
	"gopkg.in/yaml.v3"
	"github.com/go-playground/validator"
	"github.com/stretchr/testify/assert"
)

type Config struct {
	ClientID	string		`yaml:"client_id" validate:"required"`
	Enabled		bool		`yaml:"enabled"`
	DatasetID	string		`yaml:"dataset_id" validate:"required"`
	Sources		struct {}	`yaml:"sources" validate:"required"`
	Tables		struct {}	`yaml:"tables" validate:"required"`
}

var validate *validator.Validate

func TestValidateConfig(t *testing.T) {
	validate = validator.New()

	yml, err := ioutil.ReadFile("../../conf/acme/config.yml")
	if err != nil {
		log.Fatal(err)
	}

	cfg := Config{}
	err = yaml.Unmarshal(yml, &cfg)
	if err != nil {
		log.Fatal(err)
	}

	err = validate.Struct(cfg)
	assert.NoError(t, err)
	assert.Equal(t, cfg.ClientID, "acme")
	assert.Equal(t, cfg.DatasetID, "datalake_acme")
}
