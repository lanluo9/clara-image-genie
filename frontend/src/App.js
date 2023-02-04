import logo from './maple leaf.png';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
      <Box
      style={{
        backgroundColor: '#212121',
        color: '#eee',
        height: 70,
        padding: 12,
        width: 100,
      }}
    >
      <img src={logo} alt="logo" height={70} width={70}/>     
    </Box>
    <Box
      style={{
        backgroundColor: '#212121',
        color: '#eee',
        height: 70,
        padding: 12,
        width: 120,
      }}
    >
     Clara    
    </Box>
    <Box
      style={{
        backgroundColor: '#6d7377',
        color: '#ebe',
        borderRadius: 35,
        height: 50,
        width: 700,
        margin: 20,
      }}
    >  
    </Box>
      </header>      
    
      <header className="App-menubar">
      <Box
      style={{
        backgroundColor: '#6d7377',
        color: '#eee',
        height: 40,
        padding: 15,
        width: 170,
        borderRadius: 20,
        margin: 20, 
      }}
    >
     Search by Image Description 
    </Box>  
    <Box
      style={{
        backgroundColor: '#6d7377',
        color: '#eee',
        height: 40,
        padding: 15,
        width: 170,
        borderRadius: 20,
        margin: 20, 
      }}
    >
     Search by Object Recognition 
    </Box>  
    <Box
      style={{
        backgroundColor: '#6d7377',
        color: '#eee',
        height: 40,
        padding: 15,
        width: 170,
        borderRadius: 20,
        margin: 20, 
      }}
    >
     Search by OCR 
    </Box>  

      </header>

      <header className="App-body">

      </header>

    </div>

    
    
  );
}

function Box({ children, ...props }) {
  return <div {...props}>{children}</div>
}

export default App;
