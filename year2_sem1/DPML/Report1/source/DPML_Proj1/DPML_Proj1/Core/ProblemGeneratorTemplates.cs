using DPML_Proj1.CSP.Model;
using DPML_Proj1.UI.Controls.SolutionViewers;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;

namespace DPML_Proj1.Core
{
    /// <summary>
    /// This class contains concrete instances of CSP problems
    /// These are automatically scanned by the system and displayed in the UI.
    /// </summary>
    public class ProblemGeneratorTemplates
    {
        private static readonly string NL = Environment.NewLine;

        /*public static ProblemGenerator SimpleTest = new ProblemGeneratorBuilder()
            .Name("Simple Test")
            .Description("Simple arithmetic constraint system")
            .Build(_ => new ProblemBuilder()
                .Domain(Domain.IntRange(1, 5), out var dom)
                .Variable("x", dom, out var x)
                .Variable("y", dom, out var y)
                .Variable("z", dom, out var z)
                .Constraint(Constraint.Of(x, y).IntegerRelation((xVal, yVal) => xVal + yVal == 6))
                .Constraint(Constraint.Of(x, y).IntegerRelation((xVal, yVal) => xVal < yVal))
                .Constraint(Constraint.Of(z).IntegerRelation((zVal) => zVal > 3))
                .Build()
            );*/

        // simple Zebra problem for test purposes (not to be presented)
        public static ProblemGenerator Riddle3H3N = new ProblemGeneratorBuilder()
            .Name("Einstein Riddle")
            .Description(
                $"0. There are three houses, three nationals, three animals, three cigarettes.{NL}" +
                $"1.The Englishman lives in the first house on the left.{NL}" +
                $"2.In the house immediately on the right of that housing the wolf, they smoke Luky Strike.{NL}" +
                $"3.The Spaniard smokes Kent.{NL}" +
                $"4.The Russian has a horse.{NL}" +
                $"Goals: Who smokes LM? Who has the dog?"
            )
            .Build(_ => new ProblemBuilder()
                .Domain(Domain.IntRange(1, 3), out var houses)

                .Variable("Englishman", houses, out var englishman)
                .Variable("Spaniard", houses, out var spaniard)
                .Variable("Russian", houses, out var russian)

                .Variable("wolf", houses, out var wolf)
                .Variable("horse", houses, out var horse)
                .Variable("dog", houses, out var dog)

                .Variable("lucyStrike", houses, out var lucy)
                .Variable("Kent", houses, out var kent)
                .Variable("LM", houses, out var lm)

                .Constraint(Constraint.Of(englishman).Equal(1))
                .Constraint(Constraint.Of(spaniard, kent).AllEqual())
                .Constraint(Constraint.Of(russian, horse).AllEqual())
                .Constraint(Constraint.Of(wolf, lucy).IntegerRelation((hWolf, hLucy) => hLucy == hWolf + 1))

                
                .Constraint(Constraint.Of(englishman, spaniard, russian).AllUnique())
                .Constraint(Constraint.Of(wolf, horse, dog).AllUnique())
                .Constraint(Constraint.Of(lucy, kent, lm).AllUnique())

                .Build()
            );

        // Knight tour formalization attempt: backtracking is too slow even on
        // the smallest possible board. Could not be evaluated.
        public static ProblemGenerator KnightTour = new ProblemGeneratorBuilder()
            .Name("Knight tour NxM")
            .Description("Knight tour NxM")
            .Param<int>("N", 5)
            .Param<int>("M", 6)
            .Viewer<KnightTourSolutionViewer>()
            .Build(pms =>
            {
                var b = new ProblemBuilder();

                var N = pms.Get<int>("N");
                var M = pms.Get<int>("M");

                b.Domain(Domain.IntRange(0, N * M - 1), out var cellsDomain);

                var succ = new Variable[N * M];

                var moves = new (int r, int c)[]
                    {
                        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)
                    };

                for (int i = 0; i < N; i++) 
                {
                    for (int j = 0; j < M; j++)
                    {
                        var succList = new List<int>();

                        foreach ((var di, var dj) in moves)
                        {
                            int ni = i + di;
                            int nj = j + dj;
                            if (0 <= ni && ni < N && 0 <= nj && nj < M)
                            {
                                succList.Add(ni * M + nj);
                            }
                        }

                        b.Domain(Domain.FromValues(succList), out var neighborsDomain);

                        b.Variable($"succ[{i},{j}]", neighborsDomain, out succ[i * M + j]);
                    }
                }

                void PartialConnectivtyConstraint(int from, int to)
                {
                    b.Constraint(Constraint.Of(succ).IntegerRelation(vals =>
                    {
                        var visited = new HashSet<int>();

                        int current = 0;
                        for (int i = 0; i < from; i++) current = vals[current];

                        while (visited.Count < to - from) 
                        {
                            if (!visited.Add(current))
                                return false;
                            current = vals[current];
                        }
                        return true;
                    }));
                }

                for (int i = 0; i + 5 < N * M; i += 5) 
                {
                    PartialConnectivtyConstraint(i, i+5);
                }

                b.Constraint(Constraint.Of(succ).IntegerRelation(vals =>
                {
                    var visited = new HashSet<int>();

                    int current = 0;
                    while (visited.Count < N * M)
                    {
                        if (!visited.Add(current))
                            return false;
                        current = vals[current];
                    }
                    return true;
                }));

                return b.Build();
            });

        public static ProblemGenerator Picross = new ProblemGeneratorBuilder()
            .Name("Picross")
            .Description($"Picross puzzle (or Nonogram): the player has to fill an NxM white grid {NL}" +
                $"with black cells based on a list of number associated to each row/column that describe {NL}" +
                $"the lengths of continuous black stripes separated by white spaces what exist on that row/column.")
            .Viewer<PicrossSolutionViewer>()
            .Param<int>("N", 5)
            .Param<int>("M", 5)
            .Param<int[][]>("rowCues", new[]
            {
                new[] {1,1}, // first row: 2 squares separated by arbitrary space
                new[] {5},   // second row: 5 adjacent squares
                new[] {5},   // third row: 5 adjacent squares
                new[] {3},   // fourth row: 3 adjacent squares
                new[] {1},   // fourth row: 1 square
            })
            .Param<int[][]>("colCues", new[]
            {
                new[] {2},   // first row: 2 adjacent squares
                new[] {4},   // second row: 4 adjacent squares
                new[] {4},   // third row: 4 adjacent squares
                new[] {4},   // fourth row: 4 adjacent squares
                new[] {2},   // fifth row: 2 adjacent squares
            })
            .Build(pms =>
            {
                var b = new ProblemBuilder();

                var N = pms.Get<int>("N");
                var M = pms.Get<int>("M");

                var rowCues = pms.Get<int[][]>("rowCues");
                var colCues = pms.Get<int[][]>("colCues");

                // black/white or on/off grids => binary domain
                b.Domain(Domain.FromValues(new[] { 0, 1 }), out var domain);

                // variable for each cell
                var grid = new Variable[N, M];
                for (int i = 0; i < N; i++)
                {
                    for (int j = 0; j < M; j++)
                    {
                        b.Variable($"cell[{i},{j}]", domain, out grid[i, j]);
                    }
                }

                // predicate to check if a row/column of values matches the given clue
                bool MatchesClue(Value[] vals, int[] clue)
                {
                    // build the sequence of lengths of adjacent black squares separated by spaces
                    var seq = new List<int>(); 
                    int count = 0;
                    foreach (var v in vals)
                    {
                        if (v.EvaluateAs<int>() == 1)
                        {
                            count++;
                        }
                        else
                        {
                            if (count > 0)
                            {
                                seq.Add(count);
                                count = 0;
                            }
                        }
                    }
                    if (count > 0)
                        seq.Add(count);

                    // compare the obtained sequence to the clue
                    if (seq.Count != clue.Length)
                        return false;

                    for (int k = 0; k < clue.Length; k++)
                    {
                        if (seq[k] != clue[k])
                            return false;
                    }

                    return true;
                }

                // Add row constraints
                for (int i = 0; i < N; i++)
                {
                    var rowVars = Enumerable.Range(0, M).Select(j => grid[i, j]).ToArray();
                    var clue = rowCues[i];
                    b.Constraint(new FunctionConstraint(rowVars, vals => MatchesClue(vals, clue)));
                }

                // Add column constraints
                for (int j = 0; j < M; j++)
                {
                    var colVars = Enumerable.Range(0, N).Select(i => grid[i, j]).ToArray();
                    var clue = colCues[j];
                    b.Constraint(new FunctionConstraint(colVars, vals => MatchesClue(vals, clue)));
                }


                return b.Build();
            });


        public static ProblemGenerator PaleoArithmetics = new ProblemGeneratorBuilder()
           .Name("Paleo Arithmetics")
           .Description("Replace letters with digits such that SEND + MORE = MONEY")
           .Build(_ => new ProblemBuilder()
               // The usual digits domain
               .Domain(Domain.IntRange(0, 9), out var dom)
               // The first digits domain (must be non-zero)
               .Domain(Domain.IntRange(1, 9), out var domNotNull)
               // Carry domain
               .Domain(Domain.IntRange(0, 1), out var domCarry)
               // The letter variables
               .Variable("S", domNotNull, out var S)
               .Variable("E", dom, out var E)
               .Variable("N", dom, out var N)
               .Variable("D", dom, out var D)
               .Variable("M", domNotNull, out var M)
               .Variable("O", dom, out var O)
               .Variable("R", dom, out var R)
               .Variable("Y", dom, out var Y)
               // carries for each digits place jump
               .Variable("c1", domCarry, out var C1)
               .Variable("c2", domCarry, out var C2)
               .Variable("c3", domCarry, out var C3)
               .Variable("c4", domCarry, out var C4)
               // unit places constraint
               .Constraint(Constraint.Of(D, E, Y, C1).IntegerRelation((d, e, y, c1) => d + e == y + 10 * c1))
               // decimals places constraint
               .Constraint(Constraint.Of(N, R, C1, E, C2).IntegerRelation((n, r, c1, e, c2) => n + r + c1 == e + 10 * c2))
               // hundregs places constraint
               .Constraint(Constraint.Of(E, O, C2, N, C3).IntegerRelation((e, o, c2, n, c3) => e + o + c2 == n + 10 * c3))
               // thousands places constrain
               .Constraint(Constraint.Of(S, M, C3, O, C4).IntegerRelation((s, m, c3, o, c4) => s + m + c3 == o + 10 * c4))
               // Two 4-digit numbers add up to a 5-digit number, therefore, the first digit of the result must be the carry
               // [We can deduce it is actually 1 but we will let the solver find it]
               .Constraint(Constraint.Of(M, C4).IntegerRelation((m, c4) => m == c4))
               // Force all letters are different (drastically reduces solutions domain)
               .Constraint(Constraint.Of(S,E,N,D,M,O,R,Y).AllUnique())
               .Build()
           );


        public static ProblemGenerator DinosaurMystery = new ProblemGeneratorBuilder()
           .Name("Dinosaur Mystery")
           .Description(
               "Five dinosaurs (Eucentrosaurus, Hadrosaurus, Herrerasaurus, Megasaurus, Nuoerosaurus)\n" +
               "lived in Argentina, Canada, China, England, or the United States.\n" +
               "Each dinosaur lived in exactly one country, and all countries are distinct."
           )
           .Build(_ => new ProblemBuilder()
               // Countries domain
               .Domain(Domain.StringLabels("Argentina", "Canada", "China", "England", "United States"), out var countries)

               // Country variables
               .Variable("Country_Euc", countries, out var cEuc)
               .Variable("Country_Had", countries, out var cHad)
               .Variable("Country_Her", countries, out var cHer)
               .Variable("Country_Meg", countries, out var cMeg)
               .Variable("Country_Nuo", countries, out var cNuo)

               // Sizes domain: 1=smallest, 5=largest
               .Domain(Domain.IntRange(1, 5), out var sizes)

               // Size variables
               .Variable("Size_Euc", sizes, out var sEuc)
               .Variable("Size_Had", sizes, out var sHad)
               .Variable("Size_Her", sizes, out var sHer)
               .Variable("Size_Meg", sizes, out var sMeg)
               .Variable("Size_Nuo", sizes, out var sNuo)

               // All dinosaurs have unique countries
               .Constraint(Constraint.Of(cEuc, cHad, cHer, cMeg, cNuo).AllUnique())

               // All sizes are unique
               .Constraint(Constraint.Of(sEuc, sHad, sHer, sMeg, sNuo).AllUnique())

               // China dinosaur is largest
               .Constraint(Constraint.Of(cEuc, cHad, cHer, cMeg, cNuo,
                                         sEuc, sHad, sHer, sMeg, sNuo)
                   .FunctionConstraint(vals =>
                   {
                    // find the index of the China dinosaur and check if it has the largest size
                    var dCountries = vals.Take(5).Select(v => v.EvaluateAs<string>()).ToArray();
                       var dSizes = vals.Skip(5).Select(v => v.EvaluateAs<int>()).ToArray();

                       int largest = dSizes.Max();
                       int chinaIndex = Array.IndexOf(dCountries, "China");
                       if (chinaIndex < 0) return false;
                       return dSizes[chinaIndex] == largest;
                   }))

               // Herrerasaurus was the smallest
               .Constraint(Constraint.Of(sHer).Equal(1))

               // Megasaurus larger than Hadrosaurus or Eucentrosaurus
               .Constraint(Constraint.Of(sMeg, sHad).IntegerRelation((meg, hads) => meg > hads))
               .Constraint(Constraint.Of(sMeg, sEuc).IntegerRelation((meg, eu) => meg > eu))

               // China and North America (Canada or U.S.) dinosaurs were plant eaters
               // Megasaurus ate meat => Megasaurus NOT in {China, U.S., Canada}
               .Constraint(Constraint.Of(cMeg).FunctionConstraint(vals =>
               {
                   var c = vals[0].EvaluateAs<string>();
                   return c != "China" && c != "Canada" && c != "United States";
               }))

               // Eucentrosaurus lived in North America -> Canada or U.S.
               .Constraint(Constraint.Of(cEuc).FunctionConstraint(vals =>
               {
                   var c = vals[0].EvaluateAs<string>();
                   return c == "Canada" || c == "United States";
               }))

               // North America (Canada/US) and England lived later than Herrerasaurus
               // This is not about time, but the fact that Herrerasaurus is not from NA (Ca/US) or EN
               .Constraint(Constraint.Of(cHer).FunctionConstraint(vals =>
               {
                   var c = vals[0].EvaluateAs<string>();
                   return c != "Canada" && c != "United States" && c != "England";
               }))


               // Hadrosaurus lived in Argentina or the U.S.
               .Constraint(Constraint.Of(cHad).FunctionConstraint(vals =>
               {
                   var c = vals[0].EvaluateAs<string>();
                   return c == "Argentina" || c == "United States";
               }))

               .Build()
           );
    }
}
