using System;
using System.Collections.Generic;
using System.Linq;
using DPML_Proj1.CSP.Model;

namespace DPML_Proj1.CSP.Solvers
{
    public class HeuristicRepairSolver : CspSolver
    {
        private readonly int _maxIterations;
        private readonly Random _rand;

        public HeuristicRepairSolver(): this(10000) { }

        public HeuristicRepairSolver(int maxIterations, int? seed = null)
        {
            _maxIterations = maxIterations;
            _rand = seed.HasValue ? new Random(seed.Value) : new Random();
        }

        public override CspSolution Solve(Problem problem, OperationControl opc)
        {
            var variables = problem.Variables;
            // Initialize with a random complete assignment
            var currentAssignment = new Dictionary<Variable, Value>();
            foreach (var v in variables)
            {
                var vals = v.Domain.Values.ToList();
                currentAssignment[v] = vals[_rand.Next(vals.Count)];
            }

            var label = new CompoundLabel(currentAssignment.Select(Label.Of).ToArray());
            OnCandidateInspected(label);

            for (int iteration = 0; iteration < _maxIterations; iteration++)
            {
                if (problem.TestConstraints(label))
                    return Success(label);

                opc?.Check();

                // Pick a random conflicted variable
                var conflictedVars = FindConflictedVariables(problem, label).ToList();
                if (conflictedVars.Count == 0)
                    return Success(label); // all satisfied

                var varToChange = conflictedVars[_rand.Next(conflictedVars.Count)];

                // Choose the value that minimizes conflicts
                var bestValue = SelectBestValue(problem, varToChange, label, currentAssignment);

                // Assign new value
                currentAssignment[varToChange] = bestValue;
                label = new CompoundLabel(currentAssignment.Select(Label.Of).ToArray());
                OnCandidateInspected(label);
            }

            return Fail($"No solution found within {_maxIterations} iterations.");
        }

        private IEnumerable<Variable> FindConflictedVariables(Problem problem, CompoundLabel label)
        {
            foreach (var constraint in problem.Constraints)
            {
                if (!constraint.Evaluate(label))
                {
                    foreach (var v in constraint.Variables)
                        yield return v;
                }
            }
        }

        private Value SelectBestValue(
            Problem problem,
            Variable variable,
            CompoundLabel currentLabel,
            Dictionary<Variable, Value> assignment)
        {
            var domainValues = variable.Domain.Values.ToList();

            var bestScore = int.MaxValue;
            var bestValues = new List<Value>();

            foreach (var value in domainValues)
            {
                var testAssignment = new Dictionary<Variable, Value>(assignment)
                {
                    [variable] = value
                };
                var label = new CompoundLabel(testAssignment.Select(Label.Of).ToArray());
                var conflicts = CountConstraintViolations(problem, label);

                if (conflicts < bestScore)
                {
                    bestScore = conflicts;
                    bestValues.Clear();
                    bestValues.Add(value);
                }
                else if (conflicts == bestScore)
                {
                    bestValues.Add(value);
                }
            }

            // Random tie-breaking among equally good values
            return bestValues[_rand.Next(bestValues.Count)];
        }

        private int CountConstraintViolations(Problem problem, CompoundLabel label)
        {
            int count = 0;
            foreach (var constraint in problem.Constraints)
            {
                if (!constraint.Evaluate(label))
                    count++;
            }
            return count;
        }
    }
}
