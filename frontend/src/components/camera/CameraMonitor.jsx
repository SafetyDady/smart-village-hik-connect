import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import { CameraIcon, PlusCircleIcon, RefreshCcwIcon, EyeIcon } from 'lucide-react'
import { Badge } from '@/components/ui/badge.jsx'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const CameraMonitor = () => {
  const [cameras, setCameras] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCamera, setSelectedCamera] = useState(null);
  const [snapshot, setSnapshot] = useState(null);
  const [snapshotLoading, setSnapshotLoading] = useState(false);

  // Form state for adding a new camera
  const [newCamera, setNewCamera] = useState({
    name: '',
    ip_address: '',
    username: '',
    password: '',
    location: ''
  });

  // Fetch all cameras
  const fetchCameras = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/camera/status`);
      const data = await response.json();
      
      if (data.success) {
        setCameras(data.cameras);
      } else {
        setError(data.error || 'Failed to fetch cameras');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Get camera snapshot
  const getSnapshot = async (cameraId) => {
    setSnapshotLoading(true);
    try {
      const response = await fetch(`${API_URL}/camera/${cameraId}/snapshot`);
      const data = await response.json();
      
      if (data.success) {
        setSnapshot(data.image);
      } else {
        setError(data.error || 'Failed to get snapshot');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setSnapshotLoading(false);
    }
  };

  // Add a new camera
  const addCamera = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_URL}/camera/add`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newCamera),
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Reset form and refresh camera list
        setNewCamera({
          name: '',
          ip_address: '',
          username: '',
          password: '',
          location: ''
        });
        fetchCameras();
      } else {
        setError(data.error || 'Failed to add camera');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    }
  };

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewCamera(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Test camera connection
  const testConnection = async (cameraId) => {
    try {
      const response = await fetch(`${API_URL}/camera/${cameraId}/test`, {
        method: 'POST'
      });
      
      const data = await response.json();
      
      if (data.success) {
        alert('Camera connection successful!');
        fetchCameras(); // Refresh camera list to update status
      } else {
        alert('Camera connection failed: ' + (data.error || 'Unknown error'));
      }
    } catch (err) {
      alert('Network error: ' + err.message);
    }
  };

  // Load cameras on component mount
  useEffect(() => {
    fetchCameras();
  }, []);

  // Get snapshot when a camera is selected
  useEffect(() => {
    if (selectedCamera) {
      getSnapshot(selectedCamera.id);
    } else {
      setSnapshot(null);
    }
  }, [selectedCamera]);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {/* Camera List */}
      <Card className="md:col-span-1">
        <CardHeader>
          <CardTitle className="flex justify-between items-center">
            <span>กล้องทั้งหมด</span>
            <Button 
              variant="outline" 
              size="icon"
              onClick={fetchCameras}
            >
              <RefreshCcwIcon className="h-4 w-4" />
            </Button>
          </CardTitle>
          <CardDescription>กล้อง ANPR ที่ติดตั้งในหมู่บ้าน</CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex justify-center p-4">กำลังโหลด...</div>
          ) : error ? (
            <div className="text-destructive p-4">{error}</div>
          ) : cameras.length === 0 ? (
            <div className="text-center p-4">ไม่พบกล้อง</div>
          ) : (
            <div className="space-y-2">
              {cameras.map(camera => (
                <div 
                  key={camera.id}
                  className={`p-3 border rounded-lg cursor-pointer hover:bg-muted transition-colors ${selectedCamera?.id === camera.id ? 'bg-muted' : ''}`}
                  onClick={() => setSelectedCamera(camera)}
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <h3 className="font-medium">{camera.name}</h3>
                      <p className="text-sm text-muted-foreground">{camera.location}</p>
                    </div>
                    <Badge 
                      variant={camera.status === 'online' ? 'default' : 'destructive'}
                    >
                      {camera.status}
                    </Badge>
                  </div>
                  <div className="flex gap-2 mt-2">
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={(e) => {
                        e.stopPropagation();
                        testConnection(camera.id);
                      }}
                    >
                      ทดสอบ
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={(e) => {
                        e.stopPropagation();
                        getSnapshot(camera.id);
                      }}
                    >
                      <EyeIcon className="h-4 w-4 mr-1" />
                      ภาพ
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Camera Preview */}
      <Card className="md:col-span-2">
        <CardHeader>
          <CardTitle>
            {selectedCamera ? `${selectedCamera.name} - ${selectedCamera.location}` : 'เลือกกล้องเพื่อดูภาพ'}
          </CardTitle>
          <CardDescription>
            {selectedCamera ? `IP: ${selectedCamera.ip_address}` : 'กรุณาเลือกกล้องจากรายการด้านซ้าย'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {snapshotLoading ? (
            <div className="flex justify-center items-center h-64 bg-muted rounded-lg">
              กำลังโหลดภาพ...
            </div>
          ) : snapshot ? (
            <div className="flex justify-center">
              <img 
                src={snapshot} 
                alt="Camera Snapshot" 
                className="max-w-full max-h-[400px] rounded-lg shadow-md" 
              />
            </div>
          ) : (
            <div className="flex flex-col justify-center items-center h-64 bg-muted rounded-lg">
              <CameraIcon className="h-16 w-16 text-muted-foreground mb-4" />
              <p className="text-muted-foreground">ไม่มีภาพจากกล้อง</p>
            </div>
          )}
        </CardContent>
        <CardFooter>
          {selectedCamera && (
            <div className="w-full flex justify-between">
              <Button 
                variant="outline"
                onClick={() => getSnapshot(selectedCamera.id)}
                disabled={snapshotLoading}
              >
                <RefreshCcwIcon className="h-4 w-4 mr-2" />
                รีเฟรชภาพ
              </Button>
              <Button 
                variant="outline"
                onClick={() => testConnection(selectedCamera.id)}
              >
                ทดสอบการเชื่อมต่อ
              </Button>
            </div>
          )}
        </CardFooter>
      </Card>

      {/* Add New Camera Form */}
      <Card className="md:col-span-3">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <PlusCircleIcon className="h-5 w-5" />
            เพิ่มกล้องใหม่
          </CardTitle>
          <CardDescription>เพิ่มกล้อง ANPR ใหม่เข้าสู่ระบบ</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={addCamera} className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="name">ชื่อกล้อง</Label>
              <Input 
                id="name" 
                name="name" 
                placeholder="ชื่อกล้อง" 
                value={newCamera.name}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="location">ตำแหน่งติดตั้ง</Label>
              <Input 
                id="location" 
                name="location" 
                placeholder="ตำแหน่งติดตั้ง" 
                value={newCamera.location}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="ip_address">IP Address</Label>
              <Input 
                id="ip_address" 
                name="ip_address" 
                placeholder="192.168.1.100" 
                value={newCamera.ip_address}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="port">Port (Optional)</Label>
              <Input 
                id="port" 
                name="port" 
                placeholder="80" 
                value={newCamera.port || ''}
                onChange={handleInputChange}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input 
                id="username" 
                name="username" 
                placeholder="admin" 
                value={newCamera.username}
                onChange={handleInputChange}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input 
                id="password" 
                name="password" 
                type="password" 
                placeholder="••••••••" 
                value={newCamera.password}
                onChange={handleInputChange}
              />
            </div>
            <div className="md:col-span-2 flex justify-end mt-4">
              <Button type="submit">
                <PlusCircleIcon className="h-4 w-4 mr-2" />
                เพิ่มกล้อง
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default CameraMonitor

