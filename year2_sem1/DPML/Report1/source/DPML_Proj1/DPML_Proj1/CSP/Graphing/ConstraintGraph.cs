using DPML_Proj1.CSP.Model;
using DPML_Proj1.CSP.Utils;
using System.Collections.Generic;
using System.Linq;

namespace DPML_Proj1.CSP.Graphing
{
    /// <summary>
    /// Constraint graph class, only used for UI rendering and to compute nodes and edges count
    /// </summary>
    public class ConstraintGraph
    {
        public readonly Variable[] Nodes;
        public readonly Edge[] Edges;

        public class Edge
        {
            public readonly Variable From;
            public readonly Variable To;
            public readonly Constraint Constraint;

            public Edge(Variable from, Variable to, Constraint constraint)
            {
                From = from;
                To = to;
                Constraint = constraint;
            }
        }

        public ConstraintGraph(Variable[] nodes, Edge[] edges)
        {
            Nodes = nodes;
            Edges = edges;
        }

        public static ConstraintGraph FromProblem(Problem problem)
        {
            var edges = problem.Constraints
                .Select(constraint =>
                {
                    var list = new List<Edge>();
                    foreach(var (x,y) in constraint.Variables.EnumeratePairs())
                    {
                        list.Add(new Edge(x, y, constraint));
                    }
                    
                    return list;
                })
                .SelectMany(_ => _) // flatten
                .ToArray();
            return new ConstraintGraph(problem.Variables, edges);
        }

        public static (int NodesCount, int EdgesCount) ComputeConstraintGraphSize(Problem problem)
        {
            var edgesCount = problem.Constraints
                .Select(constraint =>
                {
                    var pairs = new List<(Variable, Variable)>();
                    foreach (var (x, y) in constraint.Variables.EnumeratePairs())
                    {
                        pairs.Add((x, y));
                    }
                    return pairs;
                })
                .SelectMany(_ => _)
                .Distinct()
                .Count();

            return (problem.Variables.Length, edgesCount);
        }
    }
}
