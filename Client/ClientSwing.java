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

 class PA_Client{
    Socket client;
    Scanner in;
    PrintStream out;
    public PA_Client(){}
    public void connect(String ip, int port)throws Exception{
        this.client = new Socket(ip, port);
        this.in = new Scanner(client.getInputStream());
        this.in.useDelimiter(";");
        this.out = new PrintStream(client.getOutputStream());
        System.out.println("已连接服务器，IP地址：" + this.client.getInetAddress() + "\n");
    }
    public void close() throws Exception{
        this.out.println("exit");          //发送关闭连接指令
        this.client.shutdownInput();
        this.client.shutdownOutput();
        this.client.close();
        System.out.println("服务器断开连接");
    }
    public void receive(int time)throws Exception{       //进行一次检测过程(检测数据行数)
        File file = new File("./test_data/base.tmp");   //打开缓存文件
        if(!file.getParentFile().exists()){
            file.getParentFile().mkdirs();
        }
        if(!file.exists()){
            file.createNewFile();
        }
        PrintStream writefile = new PrintStream(new FileOutputStream(file));
        this.out.println(time);                  //发送要接收的日志的时间间隔
        if(this.in.hasNext()){                   //阻塞等待服务器发送数据
            writefile.println(this.in.next());   //输出到缓存文件
        }
    }
    
    //机器学习模型分析数据
    public String analyzeData()throws Exception{
        String cmd = "./test_pa.py";
        Runtime runtime = Runtime.getRuntime();
        Process process = runtime.exec(cmd);
        if(process.waitFor() != 0){
            System.out.println("数据计算失败");
            return null;
        }
        
        Scanner scan = new Scanner(process.getInputStream());
        scan.useDelimiter("\n");
        StringBuffer buf = new StringBuffer();
        while(scan.hasNext()){
            buf.append(scan.next());
        }
        scan.close();
        return buf.toString();
    }
    
    public void timer(int s)throws Exception{
        while((s--) > 0){
            System.out.printf("等待服务器搜集日志信息:%2ds\r", s);
            Thread.sleep(1000);
        }
        System.out.println("\n");
    }
    
    public static void main(String args[]){
        PA_Client pac = new PA_Client();
        try{
            pac.connect("localhost",5973);
            pac.timer(30);
            pac.receive(10);
            System.out.println(pac.analyzeData());
        }catch(Exception e){
            System.out.println(e);
        }finally{
            try{
                pac.close();
            }catch(Exception ex){
                System.out.println(ex);
            }
        }
    }
}

public class ClientSwing {
    private JFrame frame;
    private JFrame jf;  //弹窗
    private JMenuBar menuBar;
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
    private int connect_status;
    private int start_status;
    private int countRun;
    private PA_Client client;
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
                            msgLabel.setText("(" + countRun + "/" + n + ")");
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
                        timeText.setEditable(false);
                        cntText.setEditable(false);
                        startButton.setText("结束");
                        new Thread(startRun).start();
                    }else{
                        connectButton.setEnabled(true);
                        timeText.setEditable(true);
                        cntText.setEditable(true);
                        startButton.setText("开始");
                    }
                }else{
                    msgLabel.setText("(请输入正确的值)");
                }
            }else{
                msgLabel.setText("(请先连接服务器)");
            }
        }
    };
    private ClientSwing(){
        this.frame = new JFrame("服务器电力攻击检测客户端");
        this.panel = new JPanel(null);
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
        this.client = new PA_Client();
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
                    System.out.println(text);
                    if(text != null){
                        int result = JOptionPane.showConfirmDialog(
                            jf,
                            "将会覆盖已有历史记录，确认保存？",
                            "保存检测结果",
                            JOptionPane.YES_NO_CANCEL_OPTION
                        );
                        if(result==0){
                            File file = new File("~/test_history.txt");
                            if(!file.exists()){
                                file.createNewFile();
                            }
                            PrintStream print = new PrintStream(new FileOutputStream(file));
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
                    Desktop.getDesktop().open(new File("./test_data/history.tmp"));
                }catch(IOException ioe){
                    System.out.println(ioe);
                }
            }
        });
        JMenuItem exitMenuItem = new JMenuItem("退出");
        exitMenuItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                frame.dispatchEvent(new WindowEvent(frame,WindowEvent.WINDOW_CLOSING) );
            }
        });
        fileMenu.add(saveMenuItem);
        fileMenu.addSeparator(); 
        fileMenu.add(openMenuItem);
        fileMenu.addSeparator(); 
        fileMenu.add(exitMenuItem);
        
        JMenu editMenu = new JMenu("编辑");
        JMenuItem copyMenuItem = new JMenuItem("复制数据");
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
        editMenu.add(copyMenuItem);
        
        JMenu operateMenu = new JMenu("操作");
        JMenuItem connectMenuItem = new JMenuItem("连接/断开");
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
       
        DefaultTableModel model = new DefaultTableModel();
        model.addColumn("机器学习模型计算结果");
        model.addColumn("平均负载");
        model.addColumn("CPU均值(%)");
        model.addColumn("CPU峰值(%)");
        model.addColumn("MEM均值(MB)");
        model.addColumn("NET峰值(MB/s)");
        this.table = new JTable(model);
        TableColumn firstColumn = table.getColumnModel().getColumn(0);
        firstColumn.setPreferredWidth(140);
        TableColumn secondColumn = table.getColumnModel().getColumn(1);
        secondColumn.setPreferredWidth(40);
        TableColumn sixthColumn = table.getColumnModel().getColumn(5);
        sixthColumn.setPreferredWidth(80);
        
        this.table.setPreferredScrollableViewportSize(new Dimension(580, 290));
        this.scpanel = new JScrollPane(this.table);
        this.scpanel.setBounds(10,110,580,290);
    
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
        
        this.jf = new JFrame();
        this.jf.setSize(300, 300);
        this.jf.setLocationRelativeTo(null);
        this.jf.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
                    
    }
    private void setButtunAction(){
        this.connectButton.addActionListener(connectAction);
        this.startButton.addActionListener(startAction);
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
            buf.append(this.table.getValueAt(i,j-1) + "\n");
        }
        return buf.toString();
    }
    public void init(){
        this.frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.frame.setSize(600,470);
        
        addMenuBar();
        
        placeComponents();
        
        setButtunAction();
        
        this.frame.add(this.panel);
        this.frame.setContentPane(this.panel);
        this.frame.setLocationRelativeTo(null);
        this.frame.setVisible(true);
    }
    public static void main(String[] args) {    
        new ClientSwing().init();
    }
}
