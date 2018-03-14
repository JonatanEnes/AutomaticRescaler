
# NODE LIMITS
./build/tsdb mkmetric limit.cpu.lower
./build/tsdb mkmetric limit.cpu.upper
./build/tsdb mkmetric limit.cpu.boundary
./build/tsdb mkmetric limit.mem.lower
./build/tsdb mkmetric limit.mem.upper
./build/tsdb mkmetric limit.mem.boundary
./build/tsdb mkmetric limit.disk.lower
./build/tsdb mkmetric limit.disk.upper
./build/tsdb mkmetric limit.disk.boundary
./build/tsdb mkmetric limit.net.lower
./build/tsdb mkmetric limit.net.upper
./build/tsdb mkmetric limit.net.boundary

# NODE RESOURCES
./build/tsdb mkmetric structure.cpu.current
./build/tsdb mkmetric structure.cpu.max
./build/tsdb mkmetric structure.cpu.min
./build/tsdb mkmetric structure.mem.current
./build/tsdb mkmetric structure.mem.max
./build/tsdb mkmetric structure.mem.min
./build/tsdb mkmetric structure.disk.current
./build/tsdb mkmetric structure.disk.max
./build/tsdb mkmetric structure.disk.min
./build/tsdb mkmetric structure.net.current
./build/tsdb mkmetric structure.net.max
./build/tsdb mkmetric structure.net.min
