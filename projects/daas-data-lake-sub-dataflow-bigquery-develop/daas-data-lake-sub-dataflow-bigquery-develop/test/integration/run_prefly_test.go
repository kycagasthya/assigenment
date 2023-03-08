package test

import (
	"strings"
	"testing"

	"github.com/gruntwork-io/terratest/modules/shell"
	"github.com/stretchr/testify/assert"
)

func TestRunPrefly(t *testing.T) {
	expectedText := "Done"
	cmd := shell.Command{
		Command: "python3",
		Args:    []string{"../../scripts/prefly.py", "acme"},
	}

	out := shell.RunCommandAndGetOutput(t, cmd)
	assert.Equal(t, expectedText, strings.TrimSpace(out))
}
