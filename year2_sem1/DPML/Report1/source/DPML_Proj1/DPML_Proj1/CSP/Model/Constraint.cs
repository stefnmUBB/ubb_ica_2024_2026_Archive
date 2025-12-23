using System;
using System.Collections.Generic;
using System.Linq;

namespace DPML_Proj1.CSP.Model
{
    /// <summary>
    /// Constraint involving a set of variables.
    /// Override the Evaluate() method of this class 
    /// </summary>
    public abstract class Constraint
    {
        public Variable[] Variables;

        protected Constraint(Variable[] variables)
        {
            Variables = variables;
        }

        public abstract bool Evaluate(CompoundLabel label);

        public abstract Constraint ReplaceVariables(Variable[] variables);

        /// <summary>
        /// Rebuilds the same constraint with a new set of variables.
        /// Useful when rebuilding a Problem with variables changes.
        /// </summary>
        /// <param name="newVariables"></param>
        /// <returns></returns>
        public Constraint ReplaceVariablesByName(IEnumerable<Variable> newVariables)
        {
            var vars = Variables
                .Select(oldVar => newVariables
                    .FirstOrDefault(newVar => newVar.Name == oldVar.Name) ?? throw new InvalidOperationException($"Could not find new variable by name: `{oldVar.Name}`"))
                .ToArray();
            return ReplaceVariables(vars);
        }

        public bool IsUnaryConstraintOf(Variable v) => Variables.Length == 1 && Variables[0] == v;

        public static ConstraintBuilder Of(params Variable[] vars) => new ConstraintBuilder().AddVariables(vars);

        /// <summary>
        /// Given an arbitrary compund label, this method extracts the value of the Variables associated
        /// with this constraint, in the order they appear in the array
        /// </summary>
        /// <param name="label"></param>
        /// <param name="values"></param>
        /// <returns></returns>
        protected bool ExtractValues(CompoundLabel label, out Value[] values)
        {
            values = label[Variables];
            try
            {
                values = label[Variables];
                return true;
            }
            catch(Exception e)
            {
                throw e;
                values = null;
                return false;
            }
        }
    }

    // Derived classes for generic functional constraint and only-integer constraint

    public class FunctionConstraint : Constraint
    {
        private readonly Func<Value[], bool> fEvalFunc;

        public FunctionConstraint(Variable[] variables, Func<Value[], bool> fEvalFunc)
            : base(variables)
        {
            this.fEvalFunc = fEvalFunc;
        }

        public override bool Evaluate(CompoundLabel label)
            => ExtractValues(label, out var values) && fEvalFunc(values);

        public override Constraint ReplaceVariables(Variable[] variables)
            => new FunctionConstraint(variables, fEvalFunc);
    }

    public class IntConstraint : Constraint
    {
        private readonly Func<int[], bool> fEvalFunc;

        public IntConstraint(Variable[] variables, Func<int[], bool> fEvalFunc)
            : base(variables)
        {
            this.fEvalFunc = fEvalFunc;
        }

        public override bool Evaluate(CompoundLabel label)
            => ExtractValues(label, out var values)
            && fEvalFunc(values.Select(value => value.EvaluateAs<int>()).ToArray());

        public override Constraint ReplaceVariables(Variable[] variables)
            => new IntConstraint(variables, fEvalFunc);
    }


    // factory class
    public class ConstraintBuilder
    {
        private readonly List<Variable> Variables = new List<Variable>();

        public ConstraintBuilder AddVariables(params Variable[] vars)
        {
            Variables.AddRange(vars);
            return this;
        }

        public Constraint FunctionConstraint(Func<Value[], bool> func) => new FunctionConstraint(Variables.ToArray(), func);

        public Constraint Equal<T>(T target)
        {
            AssertVarsCount(1);
            return new FunctionConstraint(Variables.ToArray(), vals => Object.Equals(target, vals[0].EvaluateAs<T>()));
        }

        public Constraint AllEqual()
        {
            return new FunctionConstraint(Variables.ToArray(), vals =>
            {
                var value = vals[0].AsObject();
                return vals.Skip(1).All(v => Object.Equals(v.AsObject(), value));
            });
        }

        public Constraint AllUnique()
        {
            return new FunctionConstraint(Variables.ToArray(), vals =>
            {
                var items = new HashSet<object>(vals.Select(v => v.AsObject()));
                return items.Count == vals.Length;
            });
        }

        public Constraint[] AllUniqueBinaryPairs()
        {
            var constraints = new List<Constraint>();

            for(int i=0;i<Variables.Count;i++)
            {
                for(int j=i+1;j<Variables.Count;j++)
                {
                    constraints.Add(new FunctionConstraint(new[] { Variables[i], Variables[j] },
                        (vals) => !Object.Equals(vals[0].AsObject(), vals[1].AsObject())));
                }
            }
            return constraints.ToArray();
        }

        public Constraint IntegerRelation(Func<int[], bool> func) => new IntConstraint(Variables.ToArray(), func);

        public Constraint IntegerRelation(Func<int, bool> func)
        {
            AssertVarsCount(1);
            return IntegerRelation(vals => func(vals[0]));
        }

        public Constraint IntegerRelation(Func<int, int, bool> func)
        {
            AssertVarsCount(2);
            return IntegerRelation(vals => func(vals[0], vals[1]));
        }

        public Constraint IntegerRelation(Func<int, int, int, bool> func)
        {
            AssertVarsCount(3);
            return IntegerRelation(vals => func(vals[0], vals[1], vals[2]));
        }

        public Constraint IntegerRelation(Func<int, int, int, int, bool> func)
        {
            AssertVarsCount(4);
            return IntegerRelation(vals => func(vals[0], vals[1], vals[2], vals[3]));
        }

        public Constraint IntegerRelation(Func<int, int, int, int, int, bool> func)
        {
            AssertVarsCount(5);
            return IntegerRelation(vals => func(vals[0], vals[1], vals[2], vals[3], vals[4]));
        }

        private void AssertVarsCount(int n)
        {
            if (Variables.Count != n)
                throw new InvalidOperationException($"Assertion failed: number of variables must be {n} for this operation (fonud {Variables.Count}).");
        }

    }

}
