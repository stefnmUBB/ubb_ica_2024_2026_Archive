using DPML_Proj1.CSP.Model;
using System.Collections.Generic;
using System.Linq;

namespace DPML_Proj1.CSP.Reducers
{
    /// <summary>
    /// Applies the AC-3 arc-consistency algorithm to prune variable domains
    /// by removing values that are not supported by any compatible assignment
    /// in their neighboring variables. Only binary constraints are considered.
    /// </summary>
    public class AC3Reducer : IReducer
    {
        public Problem Reduce(Problem problem)
        {
            // Copy domains for modification
            var domains = problem.Variables.ToDictionary(v => v, v => v.Domain.Values.ToList());

            // Collect all binary constraints
            var binaryConstraints = problem.Constraints
                .Where(c => c.Variables.Length == 2)
                .ToArray();

            if (binaryConstraints.Length == 0)
                return problem; // Nothing to do

            // Build arc queue: one arc per (Xi, Xj, constraint)
            var queue = new Queue<(Variable Xi, Variable Xj, Constraint C)>();
            foreach (var c in binaryConstraints)
            {
                var (x, y) = (c.Variables[0], c.Variables[1]);
                queue.Enqueue((x, y, c));
                queue.Enqueue((y, x, c));
            }

            while (queue.Count > 0)
            {
                var (Xi, Xj, C) = queue.Dequeue();

                if (Revise(Xi, Xj, C, domains))
                {
                    if (domains[Xi].Count == 0)
                        return problem; // domain wipeout => inconsistent

                    // Enqueue all arcs (Xk, Xi) for neighbors Xk of Xi (excluding Xj)
                    foreach (var C2 in binaryConstraints.Where(c => c.Variables.Contains(Xi) && !c.Variables.Contains(Xj)))
                    {
                        var Xk = C2.Variables.First(v => v != Xi);
                        queue.Enqueue((Xk, Xi, C2));
                    }
                }
            }

            // Build reduced problem
            var reducedVars = problem.Variables
                .Select(v => new Variable(v.Name, new Domain(domains[v])))
                .ToArray();

            var constraints = problem.Constraints
               .Select(c => c.ReplaceVariablesByName(reducedVars))
               .ToArray();

            return new Problem(reducedVars, constraints);
        }

        /// <summary>
        /// Enforces arc-consistency for the arc (Xi -> Xj) under constraint C by
        /// removing from domain of Xi any value that has no supporting value in
        /// domain of Xj that satisfies the constraint.
        /// Returns true if domain of Xi was modified, false otherwise.
        /// </summary>
        private bool Revise(Variable Xi, Variable Xj, Constraint C, Dictionary<Variable, List<Value>> domains)
        {
            bool revised = false;
            // temporary waiting list of values to remove in order
            // not to modify the containers while iterating over them
            var toRemove = new List<Value>();

            // for every value Xi can take
            foreach (var xi in domains[Xi])
            {
                bool supported = false;
                // check if we can find a value of Xj that satisfied C
                foreach (var xj in domains[Xj])
                {
                    // Build label for (Xi, Xj)
                    var label = new CompoundLabel(
                        Label.Of(Xi, xi),
                        Label.Of(Xj, xj)
                    );

                    if (C.Evaluate(label))
                    {
                        // We found xj such that Xi=xi, Xj=xj satisfies C, all good
                        supported = true;
                        break;
                    }
                }
                // if we can't find xj, remove xi from the domain
                if (!supported)
                    toRemove.Add(xi);
            }

            // remove the items we selected for remove from the domain of Xi
            if (toRemove.Count > 0)
            {
                domains[Xi].RemoveAll(toRemove.Contains);
                revised = true;
            }

            return revised;
        }
    }
}
