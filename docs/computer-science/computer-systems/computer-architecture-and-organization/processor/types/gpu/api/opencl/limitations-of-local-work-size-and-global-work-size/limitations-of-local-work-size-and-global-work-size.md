# Limitations of local work size and global work size

通常，global work size可以是任意，local work size受硬件设备所约束。在谈到local work size和global work size的限制时，一般是说local work size的限制。但是，global work size的每一个维度必须是local work size对应维度的倍数。



如果CL_DEVICE_MAX_WORK_ITEM_SIZES是[512, 512, 64]，这意味着local work size的x和y维度最大为512，z维度最大为64。

CL_DEVICE_MAX_WORK_ITEM_SIZES

CL_DEVICE_LOCAL_MEM_SIZE



对于内核local work size也有限制，CL_KERNEL_WORK_GROUP_SIZE为local work size所有维度乘积的最大值。例如CL_KERNEL_WORK_GROUP_SIZE是256，那么local work size最大为[16, 16, 1]。这是由于在线程之间分配的硬件资源有限，因此线程使用的本地内存和寄存器的数量将限制线程的数量并行执行。



可以不指定local work size，处理时会指定local work size，但是不保证是最优的

