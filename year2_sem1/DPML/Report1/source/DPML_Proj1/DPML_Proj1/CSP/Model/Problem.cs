using System.Collections.Generic;
using System.Linq;

namespace DPML_Proj1.CSP.Model
{
    /// <summary>
    /// Defines a CSP problem as a list of Variables and Constraints.
    /// The Domains are defined in the variables' scope.
    /// This is the core class used in Solvers and Reducers contracts
    /// </summary>
    public class Problem
    {
        public readonly Variable[] Variables;
        public readonly Constraint[] Constraints;

        public Problem(Variable[] variables, Constraint[] constraints)
        {
            Variables = variables;
            Constraints = constraints;
        }

        /// <summary>
        /// Checks if a compound label satisfies all the constraints
        /// (in other words, label is a solution).
        /// </summary>
        /// <param name="label"></param>
        /// <returns></returns>
        public bool TestConstraints(CompoundLabel label) => Constraints.All(c => c.Evaluate(label));

    }

    // factory class
    public class ProblemBuilder
    {
        private readonly List<Variable> Variables = new List<Variable>();
        private readonly List<Constraint> Constraints = new List<Constraint>();

        public ProblemBuilder Variable(Variable var)
        {
            Variables.Add(var);
            return this;
        }

        public ProblemBuilder Constraint(Constraint constraint)
        {
            Constraints.Add(constraint);
            return this;
        }

        public ProblemBuilder Constraint(Constraint[] constraints)
        {
            Constraints.AddRange(constraints);
            return this;
        }

        public ProblemBuilder Domain(Domain domain, out Domain outDomain)
        {
            outDomain = domain;
            return this;
        }

        public ProblemBuilder Variable(string name, Domain domain) => Variable(new Model.Variable(name, domain));

        // the "out var" clause is used to expose the variable object to be referenced later in user code (e.g. inside constraints)
        public ProblemBuilder Variable(string name, Domain domain, out Variable var) => Variable(var = new Model.Variable(name, domain));

        public Problem Build() => new Problem(Variables.ToArray(), Constraints.ToArray());

    }

}
