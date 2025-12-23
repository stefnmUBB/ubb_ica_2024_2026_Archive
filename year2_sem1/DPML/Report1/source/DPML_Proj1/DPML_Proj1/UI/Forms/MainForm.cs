using DPML_Proj1.Core;
using DPML_Proj1.UI.Controls;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DPML_Proj1.UI.Forms
{
    public partial class MainForm : Form
    {
        public MainForm()
        {
            InitializeComponent();

            ProblemGeneratorsListViewer.ProblemGeneratorSelected += ProblemGeneratorsListViewer_ProblemGeneratorSelected;

            TabControl.ClearTabs();
            LaunchProblem(ProblemGeneratorTemplates.Riddle3H3N);
        }

        private void ProblemGeneratorsListViewer_ProblemGeneratorSelected(object sender, Core.ProblemGenerator e)
        {
            LaunchProblem(e);
        }

        private void LaunchProblem(Core.ProblemGenerator problem)
        {
            TabControl.AddTab(problem.Name, new ProblemGeneratorViewer(problem));
        }
    }
}
