
The billing log format is described here: https://github.com/dCache/dcache/blob/master/skel/share/defaults/billing.properties

Message: InfoMessage
--------------------

* Attribute   Type        Description
* date        Date        Time stamp of mesage
*  cellName    CellAddress Address of cell submitting the message
* cellType    String      Type of cell submitting the message
*  session     String      Session identifier for transfer
*  type        String      Request type
*  rc          Integer     Result code
*  message     String      Message (usually error message)
*  queuingTime Long        Time request was queued (milliseconds)
*  subject     Subject     Identity of user given as a collection of
                         principals (uid, gid, FQAN, DN, Username,
                         Kerberos, Client-IP)

Message: PnfsFileInfoMessage extends InfoMessage
------------------------------------------------

* Attribute  Type        Description
* pnfsid     PnfsId      PNFS id of file
* path       String      File path
* filesize   Long        File size (bytes)
* storage    StorageInfo Storage info of file

Message: MoverInfoMessage extends PnfsFileInfoMessage
-----------------------------------------------------

* Attribute   Type        Description
*  transferred        Long         Bytes transferred
*  connectionTime     Long         Time client was connected (milliseconds)
*  created            Boolean      True on upload, false on download
*  protocol           ProtocolInfo Protocol related information
*  initiator          String       Name of cell that initiated the transfer;
                                 if p2p, begins with "pool:"; otherwise
                                 "door:"
*  p2p                Boolean      True if transfer is pool to pool
*  transferPath       String       Actual transfer path
*  meanReadBandwidth  Double       Mean of instantaneous IO bandwidth when
                                 reading (bytes/s)
*  meanWriteBandwidth Double       Mean of instantaneous IO bandwidth when
                                 writing (bytes/s)
*  readIdle           Long         Time spent not waiting disk reads to
                                 complete (ms) or '-' if there were no reads.
*  readActive         Long         Time spent waiting for disk reads to
                                 complete (ms) or '-' if there were no reads.
*  writeIdle          Long         Time spent not waiting for disk writes to
                                 complete (ms) or '-' if there were no
                                 writes.
*  writeActive        Long         Time spent waiting for disk writes to
                                 complete (ms) or '-' if there were no
                                 writes.

The "instantaneous IO bandwidth" describes the block device
performance.  It is the number bytes transferred divided by the time
taken by the block device to satisfy this request, as calculated for
each (non-empty) IO request.

Note that these bandwidth values have no provision for concurrency.
If the protocol supports concurrency and the client makes
overlapping requests then the mean bandwidth multiplied by the
"active" time may be significantly less than the number of bytes
transferred.

The four measurements (read-,write- / Idle,Active) and the two
bandwidth measurements have some uncertainty.  This comes from the
limited ability to measure precisely how long an IO operation took.
The extent of this problem depends on the operating system and the
client's activity.

Message: DoorRequestInfoMessage extends PnfsFileInfoMessage
-----------------------------------------------------------

*  Attribute         Type       Description
*  transactionTime   Long       Duration of operation (milliseconds)
*  uid               Integer    UID of user
*  gid               Integer    GID of user
*  owner             String     DN or user name
*  client            String     IP address of the client.  If the request
                              passed through one or more intermediates then
                              this is the IP address of the last
                              intermediate.
*  clientChain       String     Comma separated list of IP addresses, where the
                              first address in the list is the client or
                              intermediate connecting to dCache and the last
                              address in the list is the client initiating
                              the request.  The value of any address in the
                              list is only as reliable as any subsequent
                              intermediates handling the request.
*  transferPath      String     Actual transfer path


Message: StorageInfoMessage extends PnfsFileInfoMessage
-----------------------------------------------------------

* Attribute         Type       Description
* transferTime      Long       Duration of operation (milliseconds)


Message: RemoveFileInfoMessage extends PnfsFileInfoMessage
-----------------------------------------------------------

 No additional attributes.

Message: PoolHitInfoMessage extends PnfsFileInfoMessage
-----------------------------------------------------------

* Attribute       Type         Description
* protocol        ProtocolInfo Protocol related information
* cached          Boolean      Whether file was already online
* transferPath    String       Actual transfer path

Message: WarningPnfsFileInfoMessage extends PnfsFileInfoMessage
---------------------------------------------------------------

* Attribute       Type         Description
* transferPath    String       Actual transfer path

Type: Date
----------

 By specifying $date; format="yyyy.MM.dd HH:mm:ss:SSS"$ the date
 and time will be formatted respecting the given pattern
 "yyyy.MM.dd HH:mm:ss:SSS".  Any other date pattern can be choosen
 according to the java API SimpleDateFormat class.  The default
 pattern is for the parameter $date$ is "MM.dd HH:mm:ss".


Type: ProtocolInfo
------------------

* Field          Type              Description
* protocol       String            Protocol name (as used in pool manager)
* minorVersion   Integer           Minor version of protocol
* majorVersion   Integer           Major version of protocol
* socketAddress  InetSocketAddress IP address and port of client

Type: StorageInfo
-----------------

* Field          Type               Description
* storageClass    String            The storage class of the file
* hsm             String            HSM instance
* locations       URI[]             Tape locations
* stored          Boolean           True when stored on tape, false otherwise
* map             Map<Sting,String> Additional info as key-value pairs

Type: Subject
-------------

* Field          Type              Description
* dn             String       Distinguished name
* uid            Integer      User id
* primaryGid     Integer      Primary group id
* gids           Integer[]    Group ids
* primaryFqan    String       First FQAN (Fully Qualified Attribute Names
                             used by VOMS)
* fqans          String[]     FQANs (unsorted)
* userName       String       Mapped user name
* loginName      String       Login name

Type: PnfsId
------------

* Field          Type         Description
* databaseId     Integer      Database ID (first two bytes of PNFS ID)
* domain         String
* id             String       String form of PNFS ID
* bytes          byte[]       Binary form of PNFS ID

Type: CellAddress
------------

 The address of a cell within dCache, which may be qualified.

 If a CellAddress 'addr' is qualified then $addr.isQualified$
 expands to true, $addr.domain$ provides the domain name of this
 cell, and $addr$ expands to $addr.cell$@$addr.domain$.

 If a CellAddress 'addr' is not qualified then $addr.isQualified$
 expands to false, $addr.domain$ expands to 'local' and $addr$
 expands to $addr.cell$.

* Field          Type         Description
* cell           String       Name of the dCache cell
* domain         String       Name of the dCache domain
* isQualified    Boolean      True when the address has a domain name, false otherwise
