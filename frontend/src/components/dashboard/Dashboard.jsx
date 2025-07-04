import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { RefreshCcwIcon, CarIcon, CameraIcon, AlertCircleIcon, CheckCircleIcon } from 'lucide-react'
// Custom GateIcon
const GateIcon = (props) => (
  <svg
    {...props}
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M18 2v20M6 2v20M2 6h20M2 18h20" />
  </svg>
)
import { Badge } from '@/components/ui/badge.jsx'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const Dashboard = () => {
  const [cameras, setCameras] = useState([]);
  const [gates, setGates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastRefresh, setLastRefresh] = useState(new Date());

  // Fetch dashboard data
  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      // Fetch cameras
      const camerasResponse = await fetch(`${API_URL}/camera/status`);
      const camerasData = await camerasResponse.json();
      
      // Fetch gates
      const gatesResponse = await fetch(`${API_URL}/gate/status`);
      const gatesData = await gatesResponse.json();
      
      if (camerasData.success && gatesData.success) {
        setCameras(camerasData.cameras);
        setGates(gatesData.gates);
        setLastRefresh(new Date());
      } else {
        setError('Failed to fetch dashboard data');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Load dashboard data on component mount
  useEffect(() => {
    fetchDashboardData();
  }, []);

  // Calculate statistics
  const stats = {
    totalCameras: cameras.length,
    onlineCameras: cameras.filter(camera => camera.status === 'online').length,
    totalGates: gates.length,
    openGates: gates.filter(gate => gate.status === 'open').length,
    onlineGates: gates.filter(gate => gate.is_online).length
  };

  return (
    <div className="space-y-6">
      {/* Dashboard Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">แดชบอร์ด</h2>
          <p className="text-muted-foreground">
            อัปเดตล่าสุด: {lastRefresh.toLocaleTimeString()}
          </p>
        </div>
        <Button 
          variant="outline" 
          onClick={fetchDashboardData}
          disabled={loading}
        >
          <RefreshCcwIcon className="h-4 w-4 mr-2" />
          รีเฟรช
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">กล้องทั้งหมด</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center">
              <CameraIcon className="h-5 w-5 mr-2 text-primary" />
              <div className="text-2xl font-bold">{stats.totalCameras}</div>
              <Badge className="ml-auto" variant={stats.onlineCameras === stats.totalCameras ? 'default' : 'outline'}>
                {stats.onlineCameras} ออนไลน์
              </Badge>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">ไม้กั้นทั้งหมด</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center">
              <GateIcon className="h-5 w-5 mr-2 text-primary" />
              <div className="text-2xl font-bold">{stats.totalGates}</div>
              <Badge className="ml-auto" variant={stats.onlineGates === stats.totalGates ? 'default' : 'outline'}>
                {stats.onlineGates} ออนไลน์
              </Badge>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">สถานะไม้กั้น</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center">
              <div className={`h-3 w-3 rounded-full mr-2 ${stats.openGates > 0 ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <div className="text-2xl font-bold">{stats.openGates} / {stats.totalGates}</div>
              <Badge className="ml-auto" variant={stats.openGates > 0 ? 'default' : 'secondary'}>
                {stats.openGates > 0 ? 'เปิดอยู่' : 'ปิดทั้งหมด'}
              </Badge>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* System Status */}
      <Card>
        <CardHeader>
          <CardTitle>สถานะระบบ</CardTitle>
          <CardDescription>สถานะการทำงานของอุปกรณ์ในระบบ</CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="cameras">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="cameras" className="flex items-center gap-2">
                <CameraIcon className="h-4 w-4" />
                กล้อง ANPR
              </TabsTrigger>
              <TabsTrigger value="gates" className="flex items-center gap-2">
                <GateIcon className="h-4 w-4" />
                ไม้กั้น
              </TabsTrigger>
            </TabsList>
            
            <TabsContent value="cameras" className="mt-4">
              {loading ? (
                <div className="flex justify-center p-4">กำลังโหลด...</div>
              ) : cameras.length === 0 ? (
                <div className="text-center p-4 text-muted-foreground">ไม่พบกล้อง</div>
              ) : (
                <div className="space-y-2">
                  {cameras.map(camera => (
                    <div key={camera.id} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center">
                        {camera.status === 'online' ? (
                          <CheckCircleIcon className="h-5 w-5 mr-3 text-green-500" />
                        ) : (
                          <AlertCircleIcon className="h-5 w-5 mr-3 text-red-500" />
                        )}
                        <div>
                          <h3 className="font-medium">{camera.name}</h3>
                          <p className="text-sm text-muted-foreground">{camera.location}</p>
                        </div>
                      </div>
                      <Badge variant={camera.status === 'online' ? 'default' : 'destructive'}>
                        {camera.status}
                      </Badge>
                    </div>
                  ))}
                </div>
              )}
            </TabsContent>
            
            <TabsContent value="gates" className="mt-4">
              {loading ? (
                <div className="flex justify-center p-4">กำลังโหลด...</div>
              ) : gates.length === 0 ? (
                <div className="text-center p-4 text-muted-foreground">ไม่พบไม้กั้น</div>
              ) : (
                <div className="space-y-2">
                  {gates.map(gate => (
                    <div key={gate.id} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center">
                        {gate.is_online ? (
                          <CheckCircleIcon className="h-5 w-5 mr-3 text-green-500" />
                        ) : (
                          <AlertCircleIcon className="h-5 w-5 mr-3 text-red-500" />
                        )}
                        <div>
                          <h3 className="font-medium">{gate.name}</h3>
                          <p className="text-sm text-muted-foreground">{gate.location}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge variant={gate.is_online ? 'outline' : 'destructive'}>
                          {gate.is_online ? 'ออนไลน์' : 'ออฟไลน์'}
                        </Badge>
                        <Badge variant={gate.status === 'open' ? 'default' : 'secondary'}>
                          {gate.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>การดำเนินการด่วน</CardTitle>
          <CardDescription>ดำเนินการกับอุปกรณ์ทั้งหมดพร้อมกัน</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Button variant="outline" className="h-20 flex flex-col items-center justify-center" disabled={gates.length === 0}>
              <DoorOpenIcon className="h-6 w-6 mb-1" />
              <span>เปิดไม้กั้นทั้งหมด</span>
            </Button>
            <Button variant="outline" className="h-20 flex flex-col items-center justify-center" disabled={gates.length === 0}>
              <DoorClosedIcon className="h-6 w-6 mb-1" />
              <span>ปิดไม้กั้นทั้งหมด</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// Import missing icons
const DoorOpenIcon = (props) => (
  <svg
    {...props}
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M13 4h3a2 2 0 0 1 2 2v14" />
    <path d="M2 20h3" />
    <path d="M13 20h9" />
    <path d="M10 12v.01" />
    <path d="M13 4.562v16.157a1 1 0 0 1-1.242.97L5 20V5.562a2 2 0 0 1 1.515-1.94l4-1A2 2 0 0 1 13 4.561Z" />
  </svg>
)

const DoorClosedIcon = (props) => (
  <svg
    {...props}
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M18 20V6a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v14" />
    <path d="M2 20h20" />
    <path d="M12 12v.01" />
  </svg>
)

export default Dashboard

