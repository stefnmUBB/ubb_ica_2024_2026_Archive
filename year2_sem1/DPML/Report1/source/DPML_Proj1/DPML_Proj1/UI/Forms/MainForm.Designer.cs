
namespace DPML_Proj1.UI.Forms
{
    partial class MainForm
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

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.Body = new System.Windows.Forms.SplitContainer();
            this.Left = new System.Windows.Forms.SplitContainer();
            this.ProblemGeneratorsListViewer = new DPML_Proj1.UI.Controls.ProblemGeneratorsListViewer();
            this.TabControl = new DPML_Proj1.UI.Controls.CustomTabControl();
            ((System.ComponentModel.ISupportInitialize)(this.Body)).BeginInit();
            this.Body.Panel1.SuspendLayout();
            this.Body.Panel2.SuspendLayout();
            this.Body.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.Left)).BeginInit();
            this.Left.Panel1.SuspendLayout();
            this.Left.SuspendLayout();
            this.SuspendLayout();
            // 
            // Body
            // 
            this.Body.Dock = System.Windows.Forms.DockStyle.Fill;
            this.Body.Location = new System.Drawing.Point(0, 0);
            this.Body.Name = "Body";
            // 
            // Body.Panel1
            // 
            this.Body.Panel1.Controls.Add(this.Left);
            // 
            // Body.Panel2
            // 
            this.Body.Panel2.Controls.Add(this.TabControl);
            this.Body.Size = new System.Drawing.Size(800, 450);
            this.Body.SplitterDistance = 201;
            this.Body.TabIndex = 0;
            // 
            // Left
            // 
            this.Left.Dock = System.Windows.Forms.DockStyle.Fill;
            this.Left.Location = new System.Drawing.Point(0, 0);
            this.Left.Name = "Left";
            this.Left.Orientation = System.Windows.Forms.Orientation.Horizontal;
            // 
            // Left.Panel1
            // 
            this.Left.Panel1.Controls.Add(this.ProblemGeneratorsListViewer);
            this.Left.Size = new System.Drawing.Size(201, 450);
            this.Left.SplitterDistance = 233;
            this.Left.TabIndex = 0;
            // 
            // ProblemGeneratorsListViewer
            // 
            this.ProblemGeneratorsListViewer.Dock = System.Windows.Forms.DockStyle.Fill;
            this.ProblemGeneratorsListViewer.Location = new System.Drawing.Point(0, 0);
            this.ProblemGeneratorsListViewer.Name = "ProblemGeneratorsListViewer";
            this.ProblemGeneratorsListViewer.Size = new System.Drawing.Size(201, 233);
            this.ProblemGeneratorsListViewer.TabIndex = 0;
            // 
            // TabControl
            // 
            this.TabControl.Dock = System.Windows.Forms.DockStyle.Fill;
            this.TabControl.Location = new System.Drawing.Point(0, 0);
            this.TabControl.Name = "TabControl";
            this.TabControl.Size = new System.Drawing.Size(595, 450);
            this.TabControl.TabIndex = 0;
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.Body);
            this.Name = "MainForm";
            this.Text = "DPML Software Report 1: CSP Viewer";
            this.Body.Panel1.ResumeLayout(false);
            this.Body.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.Body)).EndInit();
            this.Body.ResumeLayout(false);
            this.Left.Panel1.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.Left)).EndInit();
            this.Left.ResumeLayout(false);
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.SplitContainer Body;
        private Controls.CustomTabControl TabControl;
        private System.Windows.Forms.SplitContainer Left;
        private Controls.ProblemGeneratorsListViewer ProblemGeneratorsListViewer;
    }
}