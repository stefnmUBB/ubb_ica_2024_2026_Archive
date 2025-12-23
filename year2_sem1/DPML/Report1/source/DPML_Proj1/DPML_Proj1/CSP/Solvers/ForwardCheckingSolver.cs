using DPML_Proj1.CSP.Model;
using System.Collections.Generic;
using System.Linq;

namespace DPML_Proj1.CSP.Solvers
{
    /// <summary>
    /// A CSP solver that performs depth-first search enhanced with
    /// forward checking. After each variable assignment, the solver
    /// proactively removes domain values of future variables that
    /// cannot participate in any valid extension of the partial
    /// assignment. If any domain becomes empty, the branch is
    /// abandoned immediately.
    /// </summary>
    public class ForwardCheckingSolver : CspSolver
    {
        public override CspSolution Solve(Problem problem, OperationControl opc)
        {
            var variables = problem.Variables;
            // Initialize working domains from original domains
            var domains = variables.ToDictionary(v => v, v => new HashSet<Value>(v.Domain.Values));

            var assignment = new List<Label>();

            var result = ForwardCheck(problem, variables, domains, assignment, opc);
            return result ?? Fail();
        }

        /// <summary>
        /// Recursive Forward Checking search procedure.
        /// Selects an unassigned variable, tries each of its current
        /// domain values, checks local consistency, prunes future domains,
        /// and recurses. Backtracks when a value cannot lead to a valid
        /// completion.
        /// </summary>
        private CspSolution ForwardCheck(
            Problem problem,
            Variable[] variables,
            Dictionary<Variable, HashSet<Value>> domains,
            List<Label> assignment,
            OperationControl opc
            )
        {
            // If all variables assigned -> check constraints and return success
            if (assignment.Count == variables.Length)
            {
                var finalLabel = new CompoundLabel(assignment.ToArray());
                if (problem.TestConstraints(finalLabel))
                    return Success(finalLabel);
                return null;
            }

            // Pick the next variable to assign
            var unassigned = variables.First(v => !assignment.Any(a => a.Variable == v));

            foreach (var value in domains[unassigned].ToList())
            {
                opc?.Check();
                var currentLabel = new CompoundLabel(assignment.Concat(new[] { Label.Of(unassigned, value) }).ToArray());
                OnCandidateInspected(currentLabel);

                // Check consistency of fully assigned constraints
                if (!IsConsistent(problem, currentLabel))
                    continue;

                // Copy domains for forward checking
                var newDomains = domains.ToDictionary(kv => kv.Key, kv => new HashSet<Value>(kv.Value));

                // Forward check: prune future domains inconsistent with current assignment
                if (!PruneFutureDomains(problem, unassigned, value, variables, assignment, newDomains))
                    continue;

                // Accept current assignment
                assignment.Add(Label.Of(unassigned, value));

                var result = ForwardCheck(problem, variables, newDomains, assignment, opc);
                if (result != null)
                    return result;

                // Revert assignment
                assignment.RemoveAll(a => a.Variable == unassigned);
            }

            return null;
        }

        /// <summary>
        /// Checks whether the partial assignment is compatible with all
        /// constraints whose variables are already fully assigned. Any
        /// violated constraint immediately invalidates the assignment.
        /// </summary>
        private bool IsConsistent(Problem problem, CompoundLabel partialLabel)
        {
            foreach (var constraint in problem.Constraints)
            {
                // If all vars of constraint are assigned, evaluate it
                if (constraint.Variables.All(v => partialLabel.Labels.Any(l => l.Variable == v)))
                {
                    if (!constraint.Evaluate(partialLabel))
                        return false;
                }
            }
            return true;
        }

        /// <summary>
        /// Performs forward checking by removing values from the domains
        /// of unassigned variables that cannot participate in a consistent
        /// extension of the current partial assignment. Only constraints
        /// involving the newly assigned variable are considered. Returns
        /// false if any domain becomes empty.
        /// </summary>
        private bool PruneFutureDomains(
            Problem problem,
            Variable currentVar,
            Value currentValue,
            Variable[] variables,
            List<Label> assignment,
            Dictionary<Variable, HashSet<Value>> domains)
        {
            var assignedLabel = Label.Of(currentVar, currentValue);
            var partialAssignment = new CompoundLabel(assignment.Concat(new[] { assignedLabel }).ToArray());

            foreach (var v in variables)
            {
                if (assignment.Any(a => a.Variable == v) || v == currentVar)
                    continue;

                var domain = domains[v];
                var toRemove = new List<Value>();

                foreach (var val in domain)
                {
                    var hypothetical = new CompoundLabel(partialAssignment.Labels.Concat(new[] { Label.Of(v, val) }).ToArray());

                    // Check all constraints involving currentVar and v
                    var relevantConstraints = problem.Constraints.Where(c =>
                        c.Variables.Contains(currentVar) && c.Variables.Contains(v));

                    bool allOk = true;
                    foreach (var constraint in relevantConstraints)
                    {
                        // If all variables of this constraint are assigned in hypothetical label -> test it
                        if (constraint.Variables.All(var => hypothetical.Labels.Any(l => l.Variable == var)))
                        {
                            if (!constraint.Evaluate(hypothetical))
                            {
                                allOk = false;
                                break;
                            }
                        }
                    }

                    if (!allOk)
                        toRemove.Add(val);
                }

                // Apply pruning
                foreach (var val in toRemove)
                    domain.Remove(val);

                if (domain.Count == 0)
                    return false; // Dead end
            }

            return true;
        }
    }
}
