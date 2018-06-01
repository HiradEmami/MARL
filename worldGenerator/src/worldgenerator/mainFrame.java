/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package worldgenerator;

import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import javax.swing.JTextField;
import java.util.ArrayList;
/**
 *
 * @author Hirad Gorgoroth
 */
public class mainFrame extends javax.swing.JFrame {
    private ArrayList<JTextField> nods;
    private int inputWidth;
    private int inputHeight;
    private int thickness;
    private int [][] dimentions;
    
    public mainFrame() {
        initComponents();
        
       
    }

     private void set_panel(String argPanel){
         switch(argPanel){
             case "goal":
                 world_panel.setVisible(false);
                 Result_panel.setVisible(false);
                 start_panel.setVisible(false);
                 obstacle_panel.setVisible(false);
                 agentPanel.setVisible(false);
                 goal_Panel.setVisible(true);
                 break;
             case "agent":
                 world_panel.setVisible(false);
                 Result_panel.setVisible(false);
                 start_panel.setVisible(false);
                 obstacle_panel.setVisible(false);
                 goal_Panel.setVisible(false);
                 agentPanel.setVisible(true);
                 break;
             case "world":
                 Result_panel.setVisible(false);
                 start_panel.setVisible(false);
                 obstacle_panel.setVisible(false);
                 agentPanel.setVisible(false);
                 goal_Panel.setVisible(false);
                 world_panel.setVisible(true);
                 break;
             case "obstacle":
                 world_panel.setVisible(false);
                 Result_panel.setVisible(false);
                 start_panel.setVisible(false);
                 agentPanel.setVisible(false);
                 goal_Panel.setVisible(false);
                 obstacle_panel.setVisible(true);
                 break;
             case "start":
                 world_panel.setVisible(false);
                 Result_panel.setVisible(false);
                 obstacle_panel.setVisible(false);
                 agentPanel.setVisible(false);
                 goal_Panel.setVisible(false);
                 start_panel.setVisible(true);
                 break;
             case "result":
                 world_panel.setVisible(false);
                 start_panel.setVisible(false);
                 obstacle_panel.setVisible(false);
                 agentPanel.setVisible(false);
                 goal_Panel.setVisible(false);
                 Result_panel.setVisible(true);                 
                 break;
         }
         
     }
     private void generateNods(int height, int weidth){
        world_panel.setLayout(new GridBagLayout());
        GridBagConstraints c = new GridBagConstraints();
        
        
        for(int i=0;i<=height-1;i++){
            for(int j=0; j<=weidth-1;j++){
              c.fill=GridBagConstraints.HORIZONTAL;
              c.gridx =j;
              c.gridy=i;
              JTextField jtextField = new JTextField();
              jtextField.setColumns(2);
              jtextField.setText("-1");
              nods.add(jtextField);
              jtextField.setHorizontalAlignment(JTextField.CENTER);
              world_panel.add(nods.get(nods.size()-1),c);
            }
        }
//          JButton button = new JButton("See the Code");
//        button.addActionListener(new ActionListener() {
//            @Override
//            public void actionPerformed(ActionEvent ae) {
//            
//            }
//        });
//         c.fill = GridBagConstraints.HORIZONTAL;
//         c.gridx=0;
//         c.gridy=height+6;
//         resultPanel.add(button, c);
        

        

    }
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jPanel4 = new javax.swing.JPanel();
        jPanel11 = new javax.swing.JPanel();
        Result_panel = new javax.swing.JPanel();
        start_panel = new javax.swing.JPanel();
        agentPanel = new javax.swing.JPanel();
        obstacle_panel = new javax.swing.JPanel();
        goal_Panel = new javax.swing.JPanel();
        world_panel = new javax.swing.JPanel();
        main_panel = new javax.swing.JPanel();
        jPanel1 = new javax.swing.JPanel();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        jPanel4.setLayout(new java.awt.CardLayout());

        javax.swing.GroupLayout jPanel11Layout = new javax.swing.GroupLayout(jPanel11);
        jPanel11.setLayout(jPanel11Layout);
        jPanel11Layout.setHorizontalGroup(
            jPanel11Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 870, Short.MAX_VALUE)
        );
        jPanel11Layout.setVerticalGroup(
            jPanel11Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 422, Short.MAX_VALUE)
        );

        jPanel4.add(jPanel11, "card8");

        javax.swing.GroupLayout Result_panelLayout = new javax.swing.GroupLayout(Result_panel);
        Result_panel.setLayout(Result_panelLayout);
        Result_panelLayout.setHorizontalGroup(
            Result_panelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 870, Short.MAX_VALUE)
        );
        Result_panelLayout.setVerticalGroup(
            Result_panelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 422, Short.MAX_VALUE)
        );

        jPanel4.add(Result_panel, "card7");

        javax.swing.GroupLayout start_panelLayout = new javax.swing.GroupLayout(start_panel);
        start_panel.setLayout(start_panelLayout);
        start_panelLayout.setHorizontalGroup(
            start_panelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 870, Short.MAX_VALUE)
        );
        start_panelLayout.setVerticalGroup(
            start_panelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 422, Short.MAX_VALUE)
        );

        jPanel4.add(start_panel, "card6");

        agentPanel.setBorder(javax.swing.BorderFactory.createBevelBorder(javax.swing.border.BevelBorder.RAISED, java.awt.Color.gray, java.awt.Color.lightGray, java.awt.Color.darkGray, java.awt.Color.gray));

        javax.swing.GroupLayout agentPanelLayout = new javax.swing.GroupLayout(agentPanel);
        agentPanel.setLayout(agentPanelLayout);
        agentPanelLayout.setHorizontalGroup(
            agentPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 866, Short.MAX_VALUE)
        );
        agentPanelLayout.setVerticalGroup(
            agentPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 418, Short.MAX_VALUE)
        );

        jPanel4.add(agentPanel, "card5");

        javax.swing.GroupLayout obstacle_panelLayout = new javax.swing.GroupLayout(obstacle_panel);
        obstacle_panel.setLayout(obstacle_panelLayout);
        obstacle_panelLayout.setHorizontalGroup(
            obstacle_panelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 870, Short.MAX_VALUE)
        );
        obstacle_panelLayout.setVerticalGroup(
            obstacle_panelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 422, Short.MAX_VALUE)
        );

        jPanel4.add(obstacle_panel, "card4");

        javax.swing.GroupLayout goal_PanelLayout = new javax.swing.GroupLayout(goal_Panel);
        goal_Panel.setLayout(goal_PanelLayout);
        goal_PanelLayout.setHorizontalGroup(
            goal_PanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 870, Short.MAX_VALUE)
        );
        goal_PanelLayout.setVerticalGroup(
            goal_PanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 422, Short.MAX_VALUE)
        );

        jPanel4.add(goal_Panel, "card3");

        javax.swing.GroupLayout world_panelLayout = new javax.swing.GroupLayout(world_panel);
        world_panel.setLayout(world_panelLayout);
        world_panelLayout.setHorizontalGroup(
            world_panelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 870, Short.MAX_VALUE)
        );
        world_panelLayout.setVerticalGroup(
            world_panelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 422, Short.MAX_VALUE)
        );

        jPanel4.add(world_panel, "card2");

        main_panel.setBackground(new java.awt.Color(204, 204, 204));
        main_panel.setBorder(javax.swing.BorderFactory.createBevelBorder(javax.swing.border.BevelBorder.RAISED, java.awt.Color.darkGray, java.awt.Color.lightGray, java.awt.Color.lightGray, java.awt.Color.darkGray));

        javax.swing.GroupLayout main_panelLayout = new javax.swing.GroupLayout(main_panel);
        main_panel.setLayout(main_panelLayout);
        main_panelLayout.setHorizontalGroup(
            main_panelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 100, Short.MAX_VALUE)
        );
        main_panelLayout.setVerticalGroup(
            main_panelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 0, Short.MAX_VALUE)
        );

        jPanel1.setBorder(javax.swing.BorderFactory.createEtchedBorder());

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 0, Short.MAX_VALUE)
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 142, Short.MAX_VALUE)
        );

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jPanel4, javax.swing.GroupLayout.PREFERRED_SIZE, 870, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addGroup(layout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(main_panel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(6, 6, 6))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(main_panel, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jPanel4, javax.swing.GroupLayout.PREFERRED_SIZE, 422, javax.swing.GroupLayout.PREFERRED_SIZE))
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(mainFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(mainFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(mainFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(mainFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new mainFrame().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JPanel Result_panel;
    private javax.swing.JPanel agentPanel;
    private javax.swing.JPanel goal_Panel;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JPanel jPanel11;
    private javax.swing.JPanel jPanel4;
    private javax.swing.JPanel main_panel;
    private javax.swing.JPanel obstacle_panel;
    private javax.swing.JPanel start_panel;
    private javax.swing.JPanel world_panel;
    // End of variables declaration//GEN-END:variables
}
