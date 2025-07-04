import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import { PlusCircleIcon, RefreshCcwIcon, DoorOpenIcon, DoorClosedIcon, AlertCircleIcon } from 'lucide-react'
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
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const GateControl = () => {
  const [gates, setGates] = useState([]);
  const [cameras, setCameras] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedGate, setSelectedGate] = useState(null);
  const [operatorName, setOperatorName] = useState('');
  const [reason, setReason] = useState('');
  const [actionLoading, setActionLoading] = useState(false);

  // Form state for adding a new gate
  const [newGate, setNewGate] = useState({
    name: '',
    location: '',
    controller_ip: '',
    controller_port: '80',
    camera_id: '',
    gate_type: 'barrier'
  });

  // Fetch all gates
  const fetchGates = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/gate/status`);
      const data = await response.json();
      
      if (data.success) {
        setGates(data.gates);
      } else {
        setError(data.error || 'Failed to fetch gates');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Fetch all cameras for selection
  const fetchCameras = async () => {
    try {
      const response = await fetch(`${API_URL}/camera/status`);
      const data = await response.json();
      
      if (data.success) {
        setCameras(data.cameras);
      }
    } catch (err) {
      console.error('Error fetching cameras:', err);
    }
  };

  // Open gate
  const openGate = async (gateId) => {
    if (!operatorName) {
      alert('กรุณาระบุชื่อผู้ควบคุม');
      return;
    }

    setActionLoading(true);
    try {
      const response = await fetch(`${API_URL}/gate/${gateId}/open`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          operator_name: operatorName,
          reason: reason || 'Manual override'
        }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        alert('เปิดไม้กั้นสำเร็จ');
        fetchGates(); // Refresh gate list to update status
      } else {
        alert('เปิดไม้กั้นไม่สำเร็จ: ' + (data.error || 'Unknown error'));
      }
    } catch (err) {
      alert('Network error: ' + err.message);
    } finally {
      setActionLoading(false);
    }
  };

  // Close gate
  const closeGate = async (gateId) => {
    if (!operatorName) {
      alert('กรุณาระบุชื่อผู้ควบคุม');
      return;
    }

    setActionLoading(true);
    try {
      const response = await fetch(`${API_URL}/gate/${gateId}/close`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          operator_name: operatorName
        }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        alert('ปิดไม้กั้นสำเร็จ');
        fetchGates(); // Refresh gate list to update status
      } else {
        alert('ปิดไม้กั้นไม่สำเร็จ: ' + (data.error || 'Unknown error'));
      }
    } catch (err) {
      alert('Network error: ' + err.message);
    } finally {
      setActionLoading(false);
    }
  };

  // Add a new gate
  const addGate = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_URL}/gate/add`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newGate),
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Reset form and refresh gate list
        setNewGate({
          name: '',
          location: '',
          controller_ip: '',
          controller_port: '80',
          camera_id: '',
          gate_type: 'barrier'
        });
        fetchGates();
      } else {
        setError(data.error || 'Failed to add gate');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    }
  };

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewGate(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Handle select changes
  const handleSelectChange = (name, value) => {
    setNewGate(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Load gates and cameras on component mount
  useEffect(() => {
    fetchGates();
    fetchCameras();
  }, []);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {/* Gate List */}
      <Card className="md:col-span-1">
        <CardHeader>
          <CardTitle className="flex justify-between items-center">
            <span>ไม้กั้นทั้งหมด</span>
            <Button 
              variant="outline" 
              size="icon"
              onClick={fetchGates}
            >
              <RefreshCcwIcon className="h-4 w-4" />
            </Button>
          </CardTitle>
          <CardDescription>ไม้กั้นที่ติดตั้งในหมู่บ้าน</CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex justify-center p-4">กำลังโหลด...</div>
          ) : error ? (
            <div className="text-destructive p-4">{error}</div>
          ) : gates.length === 0 ? (
            <div className="text-center p-4">ไม่พบไม้กั้น</div>
          ) : (
            <div className="space-y-2">
              {gates.map(gate => (
                <div 
                  key={gate.id}
                  className={`p-3 border rounded-lg cursor-pointer hover:bg-muted transition-colors ${selectedGate?.id === gate.id ? 'bg-muted' : ''}`}
                  onClick={() => setSelectedGate(gate)}
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <h3 className="font-medium">{gate.name}</h3>
                      <p className="text-sm text-muted-foreground">{gate.location}</p>
                    </div>
                    <Badge 
                      variant={gate.status === 'open' ? 'default' : 'secondary'}
                    >
                      {gate.status}
                    </Badge>
                  </div>
                  <div className="flex gap-2 mt-2">
                    <Button 
                      variant={gate.status === 'open' ? 'secondary' : 'default'}
                      size="sm"
                      onClick={(e) => {
                        e.stopPropagation();
                        if (gate.status !== 'open') {
                          openGate(gate.id);
                        }
                      }}
                      disabled={gate.status === 'open' || actionLoading}
                    >
                      <DoorOpenIcon className="h-4 w-4 mr-1" />
                      เปิด
                    </Button>
                    <Button 
                      variant={gate.status === 'closed' ? 'secondary' : 'default'}
                      size="sm"
                      onClick={(e) => {
                        e.stopPropagation();
                        if (gate.status !== 'closed') {
                          closeGate(gate.id);
                        }
                      }}
                      disabled={gate.status === 'closed' || actionLoading}
                    >
                      <DoorClosedIcon className="h-4 w-4 mr-1" />
                      ปิด
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Gate Control */}
      <Card className="md:col-span-2">
        <CardHeader>
          <CardTitle>
            {selectedGate ? `ควบคุมไม้กั้น: ${selectedGate.name}` : 'เลือกไม้กั้นเพื่อควบคุม'}
          </CardTitle>
          <CardDescription>
            {selectedGate ? `ตำแหน่ง: ${selectedGate.location} | สถานะ: ${selectedGate.status}` : 'กรุณาเลือกไม้กั้นจากรายการด้านซ้าย'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {!selectedGate ? (
            <div className="flex flex-col justify-center items-center h-64 bg-muted rounded-lg">
              <GateIcon className="h-16 w-16 text-muted-foreground mb-4" />
              <p className="text-muted-foreground">เลือกไม้กั้นเพื่อควบคุม</p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="operator_name">ชื่อผู้ควบคุม</Label>
                  <Input 
                    id="operator_name" 
                    placeholder="ระบุชื่อผู้ควบคุม" 
                    value={operatorName}
                    onChange={(e) => setOperatorName(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="reason">เหตุผลในการเปิด-ปิด (ถ้ามี)</Label>
                  <Input 
                    id="reason" 
                    placeholder="เหตุผลในการเปิด-ปิด" 
                    value={reason}
                    onChange={(e) => setReason(e.target.value)}
                  />
                </div>
              </div>
              
              <div className="p-4 bg-muted rounded-lg">
                <h3 className="font-medium mb-2">ข้อมูลไม้กั้น</h3>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div>ประเภท:</div>
                  <div>{selectedGate.gate_type}</div>
                  <div>IP Controller:</div>
                  <div>{selectedGate.controller_ip || 'ไม่มี'}</div>
                  <div>Port:</div>
                  <div>{selectedGate.controller_port}</div>
                  <div>วิธีควบคุม:</div>
                  <div>{selectedGate.control_method}</div>
                  <div>สถานะออนไลน์:</div>
                  <div>{selectedGate.is_online ? 'ออนไลน์' : 'ออฟไลน์'}</div>
                  <div>กล้องที่เชื่อมโยง:</div>
                  <div>{selectedGate.camera_id || 'ไม่มี'}</div>
                </div>
              </div>
              
              {!selectedGate.is_online && (
                <div className="flex items-center p-3 bg-destructive/10 text-destructive rounded-lg">
                  <AlertCircleIcon className="h-5 w-5 mr-2 flex-shrink-0" />
                  <p className="text-sm">ไม้กั้นออฟไลน์ การควบคุมอาจไม่ทำงาน</p>
                </div>
              )}
            </div>
          )}
        </CardContent>
        <CardFooter>
          {selectedGate && (
            <div className="w-full flex justify-between">
              <Button 
                variant="default"
                onClick={() => openGate(selectedGate.id)}
                disabled={selectedGate.status === 'open' || actionLoading || !operatorName}
                className="w-1/2 mr-2"
              >
                <DoorOpenIcon className="h-4 w-4 mr-2" />
                เปิดไม้กั้น
              </Button>
              <Button 
                variant="secondary"
                onClick={() => closeGate(selectedGate.id)}
                disabled={selectedGate.status === 'closed' || actionLoading || !operatorName}
                className="w-1/2 ml-2"
              >
                <DoorClosedIcon className="h-4 w-4 mr-2" />
                ปิดไม้กั้น
              </Button>
            </div>
          )}
        </CardFooter>
      </Card>

      {/* Add New Gate Form */}
      <Card className="md:col-span-3">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <PlusCircleIcon className="h-5 w-5" />
            เพิ่มไม้กั้นใหม่
          </CardTitle>
          <CardDescription>เพิ่มไม้กั้นใหม่เข้าสู่ระบบ</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={addGate} className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="name">ชื่อไม้กั้น</Label>
              <Input 
                id="name" 
                name="name" 
                placeholder="ชื่อไม้กั้น" 
                value={newGate.name}
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
                value={newGate.location}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="gate_type">ประเภทไม้กั้น</Label>
              <Select 
                value={newGate.gate_type} 
                onValueChange={(value) => handleSelectChange('gate_type', value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="เลือกประเภทไม้กั้น" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="barrier">ไม้กั้น (Barrier)</SelectItem>
                  <SelectItem value="sliding">ประตูเลื่อน (Sliding)</SelectItem>
                  <SelectItem value="swing">ประตูบานพับ (Swing)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="camera_id">กล้องที่เชื่อมโยง</Label>
              <Select 
                value={newGate.camera_id.toString()} 
                onValueChange={(value) => handleSelectChange('camera_id', value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="เลือกกล้อง" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">ไม่มี</SelectItem>
                  {cameras.map(camera => (
                    <SelectItem key={camera.id} value={camera.id.toString()}>
                      {camera.name} ({camera.location})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="controller_ip">IP Controller</Label>
              <Input 
                id="controller_ip" 
                name="controller_ip" 
                placeholder="192.168.1.101" 
                value={newGate.controller_ip}
                onChange={handleInputChange}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="controller_port">Port</Label>
              <Input 
                id="controller_port" 
                name="controller_port" 
                placeholder="80" 
                value={newGate.controller_port}
                onChange={handleInputChange}
              />
            </div>
            <div className="md:col-span-2 flex justify-end mt-4">
              <Button type="submit">
                <PlusCircleIcon className="h-4 w-4 mr-2" />
                เพิ่มไม้กั้น
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default GateControl

