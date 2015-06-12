from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .receipt import ReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities  import OutgoingAckProtocolEntity

class IncomingReceiptProtocolEntity(ReceiptProtocolEntity):

    '''
    delivered:
    <receipt to="xxxxxxxxxxx@s.whatsapp.net" id="1415389947-15"></receipt>

    read
    <receipt to="xxxxxxxxxxx@s.whatsapp.net" id="1415389947-15" type="read"></receipt>

    delivered to participant in group:
    <receipt participant="xxxxxxxxxx@s.whatsapp.net" from="yyyyyyyyyyyyy@g.us" id="1431204051-9" t="1431204094"></receipt>

    read by participant in group:
    <receipt participant="xxxxxxxxxx@s.whatsapp.net" t="1431204235" from="yyyyyyyyyyyyy@g.us" id="1431204051-9" type="read"></receipt>

    INCOMING
    <receipt offline="0" from="xxxxxxxxxx@s.whatsapp.net" id="1415577964-1" t="1415578027"></receipt>
    '''

    def __init__(self, _id, _from, timestamp, offline = None, type = None, participant = None):
        super(IncomingReceiptProtocolEntity, self).__init__(_id)
        self.setIncomingData(_from, timestamp, offline, type, participant)

    def getType(self):
        return self.type

    def getParticipant(self):
        return self.participant

    def getFrom(self, full = True):
        return self._from if full else self._from.split('@')[0]

    def setIncomingData(self, _from, timestamp, offline, type = None, participant = None):
        self._from = _from
        self.timestamp = timestamp
        self.type = type
        self.participant = participant
        if offline is not None:
            self.offline = True if offline == "1" else False
        else:
            self.offline = None

    def toProtocolTreeNode(self):
        node = super(IncomingReceiptProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("from", self._from)
        node.setAttribute("t", str(self.timestamp))
        if self.offline is not None:
            node.setAttribute("offline", "1" if self.offline else "0")
        if self.type is not None:
            node.setAttribute("type", self.type)
        if self.participant is not None:
            node.setAttribute("participant", self.participant)
        return node

    def __str__(self):
        out = super(IncomingReceiptProtocolEntity, self).__str__()
        out += "From: %s\n" % self._from
        out += "Timestamp: %s\n" % self.timestamp
        if self.offline is not None:
            out += "Offline: %s\n" % ("1" if self.offline else "0")
        if self.type is not None:
            out += "Type: %s\n" % (self.type)
        if self.participant is not None:
            out += "Participant: %s\n" % (self.participant)
        return out

    def ack(self):
        return OutgoingAckProtocolEntity(self.getId(), "receipt", self.getType(), self.getFrom())

    @staticmethod
    def fromProtocolTreeNode(node):
        return IncomingReceiptProtocolEntity(
            node.getAttributeValue("id"),
            node.getAttributeValue("from"),
            node.getAttributeValue("t"),
            node.getAttributeValue("offline"),
            node.getAttributeValue("type"),
            node.getAttributeValue("participant")
            )
