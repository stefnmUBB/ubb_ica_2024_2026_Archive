
namespace DPML_Proj1.UI.Controls
{
    partial class ProblemViewer
    {
        /// <summary> 
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary> 
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Component Designer generated code

        /// <summary> 
        /// Required method for Designer support - do not modify 
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.ProblemSizeLabel = new System.Windows.Forms.Label();
            this.splitContainer1 = new System.Windows.Forms.SplitContainer();
            this.tabControl1 = new System.Windows.Forms.TabControl();
            this.tabPage2 = new System.Windows.Forms.TabPage();
            this.ResetReduceButton = new System.Windows.Forms.Button();
            this.ReduceButton = new System.Windows.Forms.Button();
            this.tabPage1 = new System.Windows.Forms.TabPage();
            this.SolveContainer = new System.Windows.Forms.SplitContainer();
            this.label2 = new System.Windows.Forms.Label();
            this.OutputBox = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.SolverButton = new System.Windows.Forms.Button();
            this.ReducerOutputTextBox = new System.Windows.Forms.TextBox();
            this.GraphViewer = new DPML_Proj1.UI.Controls.ConstraintGraphControl();
            this.ReducerSelector = new DPML_Proj1.UI.Controls.ReducerSelector();
            this.SolverSelector = new DPML_Proj1.UI.Controls.SolverComboBox();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).BeginInit();
            this.splitContainer1.Panel1.SuspendLayout();
            this.splitContainer1.Panel2.SuspendLayout();
            this.splitContainer1.SuspendLayout();
            this.tabControl1.SuspendLayout();
            this.tabPage2.SuspendLayout();
            this.tabPage1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.SolveContainer)).BeginInit();
            this.SolveContainer.Panel1.SuspendLayout();
            this.SolveContainer.SuspendLayout();
            this.SuspendLayout();
            // 
            // ProblemSizeLabel
            // 
            this.ProblemSizeLabel.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.ProblemSizeLabel.AutoSize = true;
            this.ProblemSizeLabel.Location = new System.Drawing.Point(3, 182);
            this.ProblemSizeLabel.Name = "ProblemSizeLabel";
            this.ProblemSizeLabel.Size = new System.Drawing.Size(74, 13);
            this.ProblemSizeLabel.TabIndex = 0;
            this.ProblemSizeLabel.Text = "[Problem Size]";
            // 
            // splitContainer1
            // 
            this.splitContainer1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitContainer1.Location = new System.Drawing.Point(0, 0);
            this.splitContainer1.Name = "splitContainer1";
            this.splitContainer1.Orientation = System.Windows.Forms.Orientation.Horizontal;
            // 
            // splitContainer1.Panel1
            // 
            this.splitContainer1.Panel1.Controls.Add(this.GraphViewer);
            this.splitContainer1.Panel1.Controls.Add(this.ProblemSizeLabel);
            // 
            // splitContainer1.Panel2
            // 
            this.splitContainer1.Panel2.Controls.Add(this.tabControl1);
            this.splitContainer1.Size = new System.Drawing.Size(577, 415);
            this.splitContainer1.SplitterDistance = 207;
            this.splitContainer1.TabIndex = 2;
            // 
            // tabControl1
            // 
            this.tabControl1.Controls.Add(this.tabPage2);
            this.tabControl1.Controls.Add(this.tabPage1);
            this.tabControl1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tabControl1.Location = new System.Drawing.Point(0, 0);
            this.tabControl1.Name = "tabControl1";
            this.tabControl1.SelectedIndex = 0;
            this.tabControl1.Size = new System.Drawing.Size(577, 204);
            this.tabControl1.TabIndex = 2;
            // 
            // tabPage2
            // 
            this.tabPage2.Controls.Add(this.ReducerOutputTextBox);
            this.tabPage2.Controls.Add(this.ResetReduceButton);
            this.tabPage2.Controls.Add(this.ReduceButton);
            this.tabPage2.Controls.Add(this.ReducerSelector);
            this.tabPage2.Location = new System.Drawing.Point(4, 22);
            this.tabPage2.Name = "tabPage2";
            this.tabPage2.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage2.Size = new System.Drawing.Size(569, 178);
            this.tabPage2.TabIndex = 1;
            this.tabPage2.Text = "Reduce";
            this.tabPage2.UseVisualStyleBackColor = true;
            // 
            // ResetReduceButton
            // 
            this.ResetReduceButton.Location = new System.Drawing.Point(374, 35);
            this.ResetReduceButton.Name = "ResetReduceButton";
            this.ResetReduceButton.Size = new System.Drawing.Size(75, 23);
            this.ResetReduceButton.TabIndex = 2;
            this.ResetReduceButton.Text = "Reset";
            this.ResetReduceButton.UseVisualStyleBackColor = true;
            this.ResetReduceButton.Click += new System.EventHandler(this.ResetReduceButton_Click);
            // 
            // ReduceButton
            // 
            this.ReduceButton.Location = new System.Drawing.Point(374, 6);
            this.ReduceButton.Name = "ReduceButton";
            this.ReduceButton.Size = new System.Drawing.Size(75, 23);
            this.ReduceButton.TabIndex = 1;
            this.ReduceButton.Text = "Reduce";
            this.ReduceButton.UseVisualStyleBackColor = true;
            this.ReduceButton.Click += new System.EventHandler(this.ReduceButton_Click);
            // 
            // tabPage1
            // 
            this.tabPage1.Controls.Add(this.SolveContainer);
            this.tabPage1.Location = new System.Drawing.Point(4, 22);
            this.tabPage1.Name = "tabPage1";
            this.tabPage1.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage1.Size = new System.Drawing.Size(569, 178);
            this.tabPage1.TabIndex = 0;
            this.tabPage1.Text = "Solve";
            this.tabPage1.UseVisualStyleBackColor = true;
            // 
            // SolveContainer
            // 
            this.SolveContainer.Dock = System.Windows.Forms.DockStyle.Fill;
            this.SolveContainer.Location = new System.Drawing.Point(3, 3);
            this.SolveContainer.Name = "SolveContainer";
            // 
            // SolveContainer.Panel1
            // 
            this.SolveContainer.Panel1.Controls.Add(this.label2);
            this.SolveContainer.Panel1.Controls.Add(this.OutputBox);
            this.SolveContainer.Panel1.Controls.Add(this.label1);
            this.SolveContainer.Panel1.Controls.Add(this.SolverButton);
            this.SolveContainer.Panel1.Controls.Add(this.SolverSelector);
            this.SolveContainer.Size = new System.Drawing.Size(563, 172);
            this.SolveContainer.SplitterDistance = 257;
            this.SolveContainer.TabIndex = 4;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(3, 63);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(39, 13);
            this.label2.TabIndex = 4;
            this.label2.Text = "Output";
            // 
            // OutputBox
            // 
            this.OutputBox.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.OutputBox.Location = new System.Drawing.Point(46, 60);
            this.OutputBox.Multiline = true;
            this.OutputBox.Name = "OutputBox";
            this.OutputBox.ReadOnly = true;
            this.OutputBox.Size = new System.Drawing.Size(208, 109);
            this.OutputBox.TabIndex = 0;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(3, 7);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(37, 13);
            this.label1.TabIndex = 2;
            this.label1.Text = "Solver";
            // 
            // SolverButton
            // 
            this.SolverButton.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.SolverButton.Location = new System.Drawing.Point(179, 31);
            this.SolverButton.Name = "SolverButton";
            this.SolverButton.Size = new System.Drawing.Size(75, 23);
            this.SolverButton.TabIndex = 3;
            this.SolverButton.Text = "Run";
            this.SolverButton.UseVisualStyleBackColor = true;
            this.SolverButton.Click += new System.EventHandler(this.SolverButton_Click);
            // 
            // ReducerOutputTextBox
            // 
            this.ReducerOutputTextBox.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.ReducerOutputTextBox.Location = new System.Drawing.Point(6, 89);
            this.ReducerOutputTextBox.Multiline = true;
            this.ReducerOutputTextBox.Name = "ReducerOutputTextBox";
            this.ReducerOutputTextBox.ReadOnly = true;
            this.ReducerOutputTextBox.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.ReducerOutputTextBox.Size = new System.Drawing.Size(443, 83);
            this.ReducerOutputTextBox.TabIndex = 3;
            // 
            // GraphViewer
            // 
            this.GraphViewer.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.GraphViewer.BackColor = System.Drawing.SystemColors.ControlLight;
            this.GraphViewer.Graph = null;
            this.GraphViewer.Location = new System.Drawing.Point(6, 3);
            this.GraphViewer.Name = "GraphViewer";
            this.GraphViewer.Size = new System.Drawing.Size(568, 176);
            this.GraphViewer.TabIndex = 1;
            this.GraphViewer.Text = "constraintGraphControl1";
            // 
            // ReducerSelector
            // 
            this.ReducerSelector.Location = new System.Drawing.Point(6, 3);
            this.ReducerSelector.Name = "ReducerSelector";
            this.ReducerSelector.Size = new System.Drawing.Size(362, 91);
            this.ReducerSelector.TabIndex = 0;
            // 
            // SolverSelector
            // 
            this.SolverSelector.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.SolverSelector.DisplayMember = "Name";
            this.SolverSelector.FormattingEnabled = true;
            this.SolverSelector.Location = new System.Drawing.Point(46, 4);
            this.SolverSelector.Name = "SolverSelector";
            this.SolverSelector.Size = new System.Drawing.Size(208, 21);
            this.SolverSelector.TabIndex = 0;
            this.SolverSelector.SelectedIndexChanged += new System.EventHandler(this.SolverSelector_SelectedIndexChanged);
            // 
            // ProblemViewer
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.splitContainer1);
            this.Name = "ProblemViewer";
            this.Size = new System.Drawing.Size(577, 415);
            this.splitContainer1.Panel1.ResumeLayout(false);
            this.splitContainer1.Panel1.PerformLayout();
            this.splitContainer1.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).EndInit();
            this.splitContainer1.ResumeLayout(false);
            this.tabControl1.ResumeLayout(false);
            this.tabPage2.ResumeLayout(false);
            this.tabPage2.PerformLayout();
            this.tabPage1.ResumeLayout(false);
            this.SolveContainer.Panel1.ResumeLayout(false);
            this.SolveContainer.Panel1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.SolveContainer)).EndInit();
            this.SolveContainer.ResumeLayout(false);
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Label ProblemSizeLabel;
        private System.Windows.Forms.SplitContainer splitContainer1;
        private ConstraintGraphControl GraphViewer;
        private SolverComboBox SolverSelector;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button SolverButton;
        private System.Windows.Forms.SplitContainer SolveContainer;
        private System.Windows.Forms.TabControl tabControl1;
        private System.Windows.Forms.TabPage tabPage1;
        private System.Windows.Forms.TabPage tabPage2;
        private System.Windows.Forms.TextBox OutputBox;
        private System.Windows.Forms.Label label2;
        private ReducerSelector ReducerSelector;
        private System.Windows.Forms.Button ReduceButton;
        private System.Windows.Forms.Button ResetReduceButton;
        private System.Windows.Forms.TextBox ReducerOutputTextBox;
    }
}
