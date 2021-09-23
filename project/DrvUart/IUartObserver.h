#ifndef IUARTOBSERVER_H
#define IUARTOBSERVER_H

#include <cstdint>

class IUartObserver
{
public:
    virtual void i_notifySent()                        = 0;
    virtual void i_receivedByte(const uint8_t u8_byte) = 0;
    virtual void i_error(const uint8_t u8_errID)       = 0;
};

#endif // IUARTOBSERVER_H
