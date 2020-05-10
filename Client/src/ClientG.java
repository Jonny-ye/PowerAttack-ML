import javax.swing.*;
import javax.swing.table.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.datatransfer.*;
import java.net.Socket;
import java.util.Scanner;
import java.io.PrintStream;
import java.io.FileOutputStream;
import java.io.File;
import java.io.IOException;


public class ClientG{
    private JFrame frame;
    private JFrame jf;  //弹窗
    private JMenuBar menuBar;
    private JMenuItem connectMenuItem;
    private JPanel panel;
    private JScrollPane scpanel;
    private JLabel ipLabel;
    private JLabel portLabel;
    private JLabel timeLabel;
    private JLabel cntLabel;
    private JLabel statusLabel;
    private JLabel msgLabel;
    private JTable table;
    private JTextField ipText;
    private JTextField portText;      
    private JTextField timeText;
    private JTextField cntText;
    private JButton startButton;
    private JButton connectButton;
    private int connect_status; //链接状态
    private int start_status;   //检测状态
    private int countRun;
    private Client client;
    private Runnable startRun = new Runnable(){ 
        public void run(){
            try{
                int time = Integer.valueOf(timeText.getText());
                int n = Integer.valueOf(cntText.getText());
                countRun = 0;
                while(start_status%2==1 && (countRun++)<n){
                    //更新计数标签
                    SwingUtilities.invokeLater(new Runnable() {
                        public void run(){
                            msgLabel.setText("(" + String.valueOf(countRun) + " / " + String.valueOf(n) + ")");
                        }
                    });
                    //请求并接受数据
                    int t=0;
                    while(start_status%2==1 && (t++)<time){
                        Thread.sleep(1000);
                        System.out.printf("等待%2ds\r", t);
                    }
                    if(start_status%2==0){break;}
                    client.receive(time);
                    //分析数据并返回结果
                    String str = client.analyzeData();
                    SwingUtilities.invokeLater(new Runnable() {
                        public void run(){
                            DefaultTableModel dtm = (DefaultTableModel) table.getModel();
                            dtm.addRow(str.split(" "));
                            
                        }
                    });
                    SwingUtilities.invokeLater(new Runnable() {
                        public void run(){
                           JScrollBar scrollBar = scpanel.getVerticalScrollBar();
                           scrollBar.setValue(scrollBar.getMaximum());
                        }
                    });
                }
            }catch(Exception ex){
                System.out.println(ex);
            }
        }
    };
    private ActionListener connectAction = new ActionListener(){
        public void actionPerformed(ActionEvent e){
            connect_status ++;
            try{
                if(connect_status%2==1){
                    ipText.setEditable(false);
                    portText.setEditable(false);
                    String ip = ipText.getText();
                    int port = Integer.valueOf(portText.getText());
                    client.connect(ip, port);
                    statusLabel.setText("(已连接)");
                    connectButton.setText("断开");
                }
                else{
                    client.close();
                    statusLabel.setText("(已断开)");
                    ipText.setEditable(true);
                    portText.setEditable(true);
                    connectButton.setText("连接");
                }
            }catch(Exception ex){
                if(connect_status%2==1){
                    statusLabel.setText("(连接失败)");
                }else{
                    statusLabel.setText("(断开失败)");
                }
                connect_status --;
                ipText.setEditable(true);
                portText.setEditable(true);
                System.out.println(ex);
            }
        }
    };
    private ActionListener startAction = new ActionListener(){
        public void actionPerformed(ActionEvent e){
            if(connect_status%2==1){
                int time = Integer.valueOf(timeText.getText());
                int n = Integer.valueOf(cntText.getText());
                if(time>=10 && n>=1){
                    start_status++;
                    if(start_status%2==1){
                        connectButton.setEnabled(false);
                        connectMenuItem.setEnabled(false);
                        timeText.setEditable(false);
                        cntText.setEditable(false);
                        startButton.setText("结束");
                        new Thread(startRun).start();
                    }else{
                        connectButton.setEnabled(true);
                        connectMenuItem.setEnabled(true);
                        timeText.setEditable(true);
                        cntText.setEditable(true);
                        startButton.setText("开始");
                    }
                }else{
                    JOptionPane.showMessageDialog(
                            jf,
                            "请输入正确的数值（检测时间间隔>10s,检测次数>0）",
                            "提示",
                            JOptionPane.WARNING_MESSAGE
                        );
                }
            }else{
                JOptionPane.showMessageDialog(
                        jf,
                        "请先连接服务器！",
                        "提示",
                        JOptionPane.WARNING_MESSAGE
                    );
            }
        }
    };
    private ClientG(){
        this.frame = new JFrame("服务器电力攻击检测客户端");
        this.panel = new JPanel(null);
        this.jf = new JFrame();
        this.menuBar = new JMenuBar();
        this.ipLabel = new JLabel("服务器IP地址:");
        this.portLabel = new JLabel("端口：");
        this.timeLabel = new JLabel("检测时间间隔(>10s):");
        this.cntLabel = new JLabel("检测次数:");
        this.statusLabel = new JLabel("(未连接)");
        this.ipText = new JTextField("127.0.0.1",15);
        this.portText = new JTextField("5973",4);       
        this.timeText = new JTextField("30",3);
        this.cntText = new JTextField("5",3);
        this.msgLabel = new JLabel("( 0 / 5 )");
        this.startButton = new JButton("开始");
        this.connectButton = new JButton("连接");
        this.client = new Client();
        this.connect_status = 0;
        this.start_status = 0;
        this.countRun = 0;
    }
    private void addMenuBar(){
        JMenu fileMenu = new JMenu("文件");
        JMenuItem saveMenuItem = new JMenuItem("保存结果");
        saveMenuItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                try{
                    String text = getTableData();
                    if(text != null){
                        int result = JOptionPane.showConfirmDialog(
                            jf,
                            "将会覆盖已有文件（位置：./test_history.txt），确认保存？",
                            "保存检测结果",
                            JOptionPane.YES_NO_CANCEL_OPTION
                        );
                        if(result==0){
                            File file = new File("./test_history.txt");
                            if(!file.exists()){
                                file.createNewFile();
                            }
                            PrintStream print = new PrintStream(new FileOutputStream(file));
                            print.println(text);
                        }
                    }else{
                        JOptionPane.showMessageDialog(
                            jf,
                            "检测结果为空！",
                            "提示",
                            JOptionPane.WARNING_MESSAGE
                        );
                    }
                }catch(IOException ioe){
                    System.out.println(ioe);
                }
            }
        });
        JMenuItem openMenuItem = new JMenuItem("历史数据");
        openMenuItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                try{
                    File file = new File("./test_data/history.tmp");
                    if(!file.getParentFile().exists()){
                        file.getParentFile().mkdirs();
                    }
                    if(!file.exists()){
                        file.createNewFile();
                    }
                    Desktop.getDesktop().open(file);
                }catch(IOException ioe){
                    System.out.println(ioe);
                }
            }
        });
        JMenuItem exitMenuItem = new JMenuItem("退出");
        exitMenuItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                int result = JOptionPane.showConfirmDialog(
                        jf,
                        "确认退出？",
                        "提示",
                        JOptionPane.YES_NO_CANCEL_OPTION
                    );
                if(result==0){
                    frame.dispatchEvent(new WindowEvent(frame,WindowEvent.WINDOW_CLOSING) );
                }
            }
        });
        fileMenu.add(saveMenuItem);
        fileMenu.add(openMenuItem);
        fileMenu.addSeparator(); 
        fileMenu.add(exitMenuItem);
        
        JMenu editMenu = new JMenu("编辑");
       JMenuItem copyMenuItem = new JMenuItem("复制");
         copyMenuItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                String text = getTableData();
                if(text != null){
                    Clipboard clipboard = Toolkit.getDefaultToolkit().getSystemClipboard();
                    Transferable trans = new StringSelection(text);
                    clipboard.setContents(trans, null);
                }else{
                    JOptionPane.showMessageDialog(
                        jf,
                        "检测结果为空！",
                        "提示",
                        JOptionPane.WARNING_MESSAGE
                    );
                }
            }
        });
        JMenuItem cleanMenuItem = new JMenuItem("清空");
         cleanMenuItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                String text = getTableData();
                if(text != null){
                    int result = JOptionPane.showConfirmDialog(
                            jf,
                            "将会清空所有检测结果，是否继续？",
                            "清空",
                            JOptionPane.YES_NO_CANCEL_OPTION
                        );
                    if(result==0){
                        DefaultTableModel model = (DefaultTableModel)table.getModel();
                        for( int i = model.getRowCount() - 1; i >= 0; i-- ) {
                            model.removeRow(i);
                        }
                    }
                }else{
                    JOptionPane.showMessageDialog(
                        jf,
                        "检测结果为空！",
                        "提示",
                        JOptionPane.WARNING_MESSAGE
                    );
                }
            }
        });
        editMenu.add(copyMenuItem);
        editMenu.addSeparator(); 
        editMenu.add(cleanMenuItem);
        
        JMenu operateMenu = new JMenu("操作");
        connectMenuItem = new JMenuItem("连接/断开");
        connectMenuItem.addActionListener(connectAction);
        JMenuItem startMenuItem = new JMenuItem("开始/结束");
        startMenuItem.addActionListener(startAction);
        
        operateMenu.add(connectMenuItem);
        operateMenu.addSeparator(); 
        operateMenu.add(startMenuItem);
        
        
        JMenu aboutMenu = new JMenu("关于");
        JMenuItem settingMenuItem = new JMenuItem("设置");
        settingMenuItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                 JOptionPane.showMessageDialog(
                        jf,
                        "请在界面中设置数值",
                        "设置",
                        JOptionPane.INFORMATION_MESSAGE
                    );
            }
        });
        JMenuItem aboutMenuItem = new JMenuItem("关于客户端");
        aboutMenuItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                JOptionPane.showMessageDialog(
                        jf,
                        "基于机器学习(BP神经网络)数据中心电力攻击检测客户端\n版本：1.0\n作者：Jonny-ye (HDU)\n网站：https://github.com/Jonny-ye/PowerAttack-ML\n",
                        "关于客户端",
                        JOptionPane.INFORMATION_MESSAGE
                    );
             }
        });
        aboutMenu.add(settingMenuItem);
        aboutMenu.addSeparator(); 
        aboutMenu.add(aboutMenuItem);
        
        this.menuBar.add(fileMenu);
        this.menuBar.add(editMenu);
        this.menuBar.add(operateMenu);
        this.menuBar.add(aboutMenu);
        this.frame.setJMenuBar(this.menuBar);
    }
    private  void placeComponents(){
    
        this.ipLabel.setBounds(30,20,100,30);
        this.ipText.setBounds(120,20,100,30);
        this.portLabel.setBounds(260,20,40,30);
        this.portText.setBounds(300,20,60,30);
        this.statusLabel.setBounds(390,20,110,30);
        this.connectButton.setBounds(500,20,70,30);
        this.timeLabel.setBounds(30,60,120,30);
        this.timeText.setBounds(160,60,60,30);
        this.cntLabel.setBounds(240,60,60,30);
        this.cntText.setBounds(300,60,60,30);
        this.msgLabel.setBounds(390,60,110,30);
        this.startButton.setBounds(500,60,70,30);
        
        this.connectButton.addActionListener(connectAction);
        this.startButton.addActionListener(startAction);
        
        DefaultTableModel model = new DefaultTableModel();
        model.addColumn("机器学习模型计算结果");
        model.addColumn("平均功耗(W)");
        model.addColumn("CPU均值(%)");
        model.addColumn("CPU峰值(%)");
        model.addColumn("内存均值(MB)");
        model.addColumn("网络峰值(MB/s)");
        this.table = new JTable(model);
        TableColumn firstColumn = table.getColumnModel().getColumn(0);
        firstColumn.setPreferredWidth(125);
        TableColumn secondColumn = table.getColumnModel().getColumn(1);
        secondColumn.setPreferredWidth(55);
        TableColumn sixthColumn = table.getColumnModel().getColumn(5);
        sixthColumn.setPreferredWidth(80);
        
        this.table.setPreferredScrollableViewportSize(new Dimension(580, 300));
        this.scpanel = new JScrollPane(this.table);
        this.scpanel.setBounds(10,110,580,300);
    
        this.panel.add(this.ipLabel);
        this.panel.add(this.ipText);
        this.panel.add(this.portLabel);
        this.panel.add(this.portText);
        this.panel.add(this.connectButton);
        this.panel.add(this.timeLabel);
        this.panel.add(this.timeText);
        this.panel.add(this.cntLabel);
        this.panel.add(this.cntText);
        this.panel.add(this.msgLabel);
        this.panel.add(this.startButton);
        this.panel.add(this.statusLabel);
        this.panel.add(this.scpanel);
        
        this.jf.setSize(300, 300);
        this.jf.setLocationRelativeTo(null);
        this.jf.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
    }
    private String getTableData(){
        if(this.table.getRowCount()==0){
            return null;
        }
        StringBuffer buf = new StringBuffer();
        for(int i=0; i<this.table.getRowCount(); i++){
            int j=0;
            for(; j<this.table.getColumnCount()-1; j++){
                buf.append(this.table.getValueAt(i,j) + ",");
            }
            buf.append(this.table.getValueAt(i,j) + "\n");
        }
        return buf.toString();
    }
    public void init(){
        this.frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.frame.setSize(600,480);
        placeComponents();
        addMenuBar();
        this.frame.add(this.panel);
        this.frame.setContentPane(this.panel);
        this.frame.setLocationRelativeTo(null);
        this.frame.setVisible(true);
    }
    public static void main(String[] args) {    
        new ClientG().init();
    }
}
