import { useState } from 'react';
import { Chat } from './components/Chat';
import { Dashboard } from './components/Dashboard';

function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleTraceAdded = () => {
    // Trigger dashboard refresh
    setRefreshKey(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-slate-100 font-sans flex justify-center">
      <div className="w-full max-w-[1600px] flex p-4 lg:p-6 gap-6 flex-col lg:flex-row">
        {/* Chat Section */}
        <div className="w-full lg:w-[400px] xl:w-[480px] h-[600px] lg:h-[calc(100vh-48px)] flex-shrink-0">
          <Chat onTraceAdded={handleTraceAdded} />
        </div>

        {/* Dashboard Section */}
        <div className="flex-1 min-w-0 h-[800px] lg:h-[calc(100vh-48px)]">
          <Dashboard refreshKey={refreshKey} />
        </div>
      </div>
    </div>
  );
}

export default App;
