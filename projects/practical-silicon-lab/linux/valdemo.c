// 실제 Linux misc character driver. 외부 하드웨어 없이 I/O 경로를 설명한다.
#include <linux/module.h>
#include <linux/miscdevice.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/mutex.h>

static DEFINE_MUTEX(state_lock);
static u64 sequence;
static u32 last_sum;
static size_t last_length;

static ssize_t val_write(struct file *file, const char __user *user,
                         size_t count, loff_t *position)
{
    u8 payload[256];
    u32 sum = 0;
    size_t i;

    if (count == 0 || count > sizeof(payload))
        return -EMSGSIZE;  // 허용 범위를 벗어나면 일부만 처리하지 않는다.
    if (copy_from_user(payload, user, count))
        return -EFAULT;    // user pointer를 직접 역참조하지 않는다.

    for (i = 0; i < count; ++i)
        sum += payload[i];

    // 여러 process가 write해도 하나의 완전한 결과로 갱신한다.
    mutex_lock(&state_lock);
    last_sum = sum;
    last_length = count;
    sequence++;
    mutex_unlock(&state_lock);
    return count;         // byte 수를 반환한다. 0은 성공 byte 수가 아니다.
}

static ssize_t val_read(struct file *file, char __user *user,
                        size_t count, loff_t *position)
{
    char result[96];
    int length;

    mutex_lock(&state_lock);
    length = scnprintf(result, sizeof(result),
        "sequence=%llu length=%zu sum=%u\n",
        (unsigned long long)sequence, last_length, last_sum);
    mutex_unlock(&state_lock);
    // file offset을 갱신해 동일한 열린 파일의 다음 read는 EOF에 도달한다.
    return simple_read_from_buffer(user, count, position, result, length);
}

static const struct file_operations val_ops = {
    .owner = THIS_MODULE,  // 열린 file이 있는 동안 module 수명을 보호한다.
    .read = val_read,
    .write = val_write,
    .llseek = NULL,        // seek 동작을 제공하지 않는다.
};

static struct miscdevice val_device = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = "valdemo",
    .fops = &val_ops,
    .mode = 0600,
};

static int __init val_init(void)
{
    int error = misc_register(&val_device);
    if (!error)
        pr_info("valdemo: ready, software-backed device\n");
    return error;  // 등록 실패를 숨기면 /dev 경로만 조사하게 된다.
}

static void __exit val_exit(void)
{
    misc_deregister(&val_device);
}

module_init(val_init);
module_exit(val_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Software-backed validation I/O teaching device");
