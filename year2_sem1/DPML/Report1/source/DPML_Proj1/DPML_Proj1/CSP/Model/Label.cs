using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace DPML_Proj1.CSP.Model
{
    /// <summary>
    /// Label class defines an association (assignment) between a variable and a value
    /// </summary>
    public class Label
    {
        public readonly Variable Variable;
        public readonly Value Value;

        public Label(Variable variable, Value value)
        {
            Variable = variable;
            Value = value;
        }

        public static Label Of(Variable variable, Value value) => new Label(variable, value);
        public static Label Of(KeyValuePair<Variable, Value> tuple) => new Label(tuple.Key, tuple.Value);

        public override string ToString() => $"({Variable.Name}: {Value})";
    }

    /// <summary>
    /// Collection of zero, one or more labels
    /// </summary>
    public class CompoundLabel
    {
        public readonly Label[] Labels;

        public CompoundLabel(params Label[] labels)
        {
            Labels = labels;
        }

        // easy access of variables inside, e.g. compLabel[varObj] or compLabel["varName"]

        public Value this[Variable var] => Labels
            .FirstOrDefault(label=>label.Variable==var)?.Value
            ?? throw new VariableNotFoundException(this, var);

        public Value[] this[Variable[] vars] => vars
            .Select(var => Labels.FirstOrDefault(label => label.Variable == var)?.Value ?? throw new VariableNotFoundException(this, var))
            .ToArray();

        public Value this[string varName] => Labels.FirstOrDefault(label => label.Variable.Name == varName)?.Value
            ?? throw new VariableNotFoundException(this, varName);

        public Value GetValueOrNull(string varName) => Labels.FirstOrDefault(label => label.Variable.Name == varName)?.Value;

        public override string ToString() => $"({string.Join(", ", Labels.Select(_ => _.ToString()))})";
    }

    public class VariableNotFoundException : Exception
    {
        public VariableNotFoundException(CompoundLabel label, Variable v)
            : base($"Attempted to read variable {v} from {label}") { }

        public VariableNotFoundException(CompoundLabel label, string varName)
            : base($"Attempted to read variable `{varName}` from {label}") { }
    }
}
