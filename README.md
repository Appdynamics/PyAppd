# PyAppd
Python API for AppDynamics REST API


### Example: Pull all JVM parameters from Mulesoft Nodes
Start by importing my helper module.  This will make your life a little easier especially if your API client has a short lived TTL.  The helper checks to see if the token has expired and automatically refreshes the auth token if necessary


```python
from pyappd import PyAppdApi
import csv
import sys
print(sys.version)
```

    3.7.8 (default, Jul  4 2020, 10:17:17) 
    [Clang 11.0.3 (clang-1103.0.32.62)]


#### Get an API Object
You must use an API client as opposed to user / password.  


```python
omf = PyAppdApi("https://onemain-test.saas.appdynamics.com", "TestRKR")
```

    Enter Client Secret ····································


#### Print a list of Apps and Tiers Defined in this Controller


```python
for app in omf.getApps():
    print(f"{'Application':25}{'AppID':8}{'Tier':35}{'TierID':8}{'NodeCount':6}")    
    tiers = omf.getTiers(app)
    for tier in tiers:
        print(f"{app['name']:25}{app['id']:<8}{tier['name']:<35}{tier['id']!s:<8}{tier['numberOfNodes']!s:<6}")
    print()
```

    Application              AppID   Tier                               TierID  NodeCount
    Enterprise Portal Apps   31258   Portal                             915412  4     
    Enterprise Portal Apps   31258   elf                                860747  2     
    
    Application              AppID   Tier                               TierID  NodeCount
    Kofax                    31171   Default Web Site                   794467  6     
    Kofax                    31171   Default Web Site/TotalAgility      792423  6     
    Kofax                    31171   Kofax Extraction Service           798903  35    
    Kofax                    31171   Kofax Transformation Service       792929  4     
    Kofax                    31171   Kofax Web/App Core Worker Service  799180  0     
    Kofax                    31171   Machine Agent                      792418  0     
    
    Application              AppID   Tier                               TierID  NodeCount
    Mobius                   31206   Test 6                             915389  0     
    Mobius                   31206   VDRNets                            821087  3     
    Mobius                   31206   VDRWS                              1064486 0     
    Mobius                   31206   elf                                838061  0     
    Mobius                   31206   mobius-view                        820671  2     
    Mobius                   31206   moses                              826417  2     
    Mobius                   31206   om-apps                            820905  0     
    
    Application              AppID   Tier                               TierID  NodeCount
    Mulesoft                 21577   acctapi                            266649  2     
    Mulesoft                 21577   acctapi-a                          267863  2     
    Mulesoft                 21577   acctapi-b                          361513  2     
    Mulesoft                 21577   acctapi-c                          538674  2     
    Mulesoft                 21577   applapi                            267090  2     
    Mulesoft                 21577   applapi-a                          267896  2     
    Mulesoft                 21577   applapi-b                          361516  2     
    Mulesoft                 21577   applapi-c                          538673  2     
    Mulesoft                 21577   brnapi                             266650  2     
    Mulesoft                 21577   brnapi-a                           267891  2     
    Mulesoft                 21577   docapi                             443265  4     
    Mulesoft                 21577   docapi-a                           442760  4     
    Mulesoft                 21577   docapi-b                           443272  4     
    Mulesoft                 21577   docapi-c                           443275  4     
    Mulesoft                 21577   docapi-d                           724768  4     
    Mulesoft                 21577   docapi2                            538152  2     
    Mulesoft                 21577   docapi2-a                          538153  2     
    Mulesoft                 21577   empapi                             267141  2     
    Mulesoft                 21577   empapi-a                           267906  2     
    Mulesoft                 21577   techapi                            266652  2     
    Mulesoft                 21577   techapi-a                          267898  2     
    Mulesoft                 21577   techapi-b                          360656  2     
    Mulesoft                 21577   techapi-c                          443277  2     
    Mulesoft                 21577   techapi-d                          725064  2     
    
    Application              AppID   Tier                               TierID  NodeCount
    RKR_Ruby                 31755   SpreeTier                          1000954 0     
    
    Application              AppID   Tier                               TierID  NodeCount
    RubyStaging              31822   FrontEnd                           1028003 2     
    RubyStaging              31822   FrontEnd - Sidekiq                 1028060 1     
    
    Application              AppID   Tier                               TierID  NodeCount
    appserver                31862   metric-ingestor                    1038882 1     
    
    Application              AppID   Tier                               TierID  NodeCount
    class                    31861   metric-ingestor                    1038860 1     
    
    Application              AppID   Tier                               TierID  NodeCount
    eSign                    15789   DocEngine                          541735  0     
    eSign                    15789   ESIG_ADMDYNCLR                     73643   1     
    eSign                    15789   ESIG_APPLICATION                   73646   6     
    eSign                    15789   ESIG_PLATFORM                      73644   12    
    eSign                    15789   OMF_ESIG_APPLICATIONS              73647   9     
    eSign                    15789   RCSMGRSVR                          261778  1     
    
    Application              AppID   Tier                               TierID  NodeCount
    mainframe                31863   metric-ingestor                    1038883 1     
    
    Application              AppID   Tier                               TierID  NodeCount
    metric-ingestor          31687   metric-ingestor                    915318  1     
    


#### Get the Mule Nodes


```python
muleApp = omf.searchArray(omf.getApps(), "name","Mulesoft")
muleTiers = omf.getTiers(muleApp)
muleNodes = []
for tier in muleTiers:
    muleNodes.extend(omf.getNodes(muleApp, tier))
nodeJVM = []
for node in muleNodes:
    nodeJVM.append(omf.getJVMDetailsForNode(node))
```


```python
columns = set()
for node in nodeJVM:
    for prop in node["latestVmSystemProperties"]:
        columns.add(prop['name'])
data = []
for node in nodeJVM:
    row = []
    for col in columns:
        value = omf.searchArray(node['latestVmSystemProperties'], "name", col)
        row.append(value['value'] if value else "N/A")
    data.append(row)

with open ("out.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(data)
```


```python
with open('out.csv', 'r') as file:
    print(file.readline())
    print(file.readline())
```

    wrapper.native_library,java.vm.info,mule.metadata.cache.expirationInterval.millis,sun.os.patch.level,java.vendor,wrapper.lang.folder,java.vendor.url.bug,java.home,log4j2.loggerContextFactory,user.language,org.glassfish.grizzly.nio.transport.TCPNIOTransport.max-send-buffer-size,anypoint.platform.base_uri,appdynamics.agent.uniqueHostId,appdynamics.agent.maxMetrics,java.vm.vendor,awt.toolkit,wrapper.arch,java.endorsed.dirs,java.vm.specification.vendor,sun.nio.ch.bugLevel,java.class.version,sun.boot.class.path,wrapper.lang.domain,java.vm.name,sun.jnu.encoding,appdynamics.async.instrumentation.strategy,anypoint.platform.analytics_base_uri,mvel2.disable.jit,appdynamics.log4j2.disable.jmx,org.quartz.scheduler.skipUpdateCheck,AsyncLoggerConfig.ExceptionHandler,java.vm.specification.name,log4j.configurationFactory,java.vendor.url,wrapper.pid,mule.encoding,java.runtime.name,mule.metadata.cache.entryTtl.minutes,appdynamics.agent.nodeName,java.awt.printerjob,anypoint.platform.client_id,anypoint.platform.client_secret,file.separator,path.separator,org.apache.commons.logging.LogFactory,log4j2.disable.jmx,java.class.path,wrapper.version,wrapper.jvmid,java.specification.version,line.separator,sun.boot.library.path,sun.java.command,com.ibm.mq.cfg.useIBMCipherMappings,xpath.provider,sun.cpu.isalist,mule.base,java.awt.graphicsenv,java.ext.dirs,wrapper.backend,wrapper.java.pid,mule.env,java.library.path,sun.java.launcher,os.name,user.timezone,file.encoding.pkg,MULE_CONFIG_PATH,wrapper.key,file.encoding,java.version,os.arch,user.name,appdynamics.agent.tierName,sun.arch.data.model,sun.cpu.endian,mule.home,java.io.tmpdir,appdynamics.agent.log4j2.disabled,org.glassfish.grizzly.nio.transport.TCPNIOTransport.max-receive-buffer-size,sun.management.compiler,java.vm.version,wrapper.service,user.home,java.util.prefs.PreferencesFactory,mule.agent.configuration.folder,sun.io.unicode.encoding,wrapper.cpu.timeout,java.runtime.version,MULE_ENV,user.dir,java.specification.name,java.vm.specification.version,java.locale.providers,wrapper.disable_console_input,os.version,user.country,java.specification.vendor,java.net.preferIPv4Stack
    
    wrapper,mixed mode,5000,unknown,Oracle Corporation,../lang,http://bugreport.sun.com/bugreport/,/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.265.b01-1.el7_9.ppc64le/jre,N/A,en,1048576,https://anypoint.mulesoft.com,evpmulet102.corp.fin,6000,Oracle Corporation,sun.awt.X11.XToolkit,ppcle,/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.265.b01-1.el7_9.ppc64le/jre/lib/endorsed,Oracle Corporation,N/A,52.0,/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.265.b01-1.el7_9.ppc64le/jre/lib/resources.jar:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.265.b01-1.el7_9.ppc64le/jre/lib/rt.jar:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.265.b01-1.el7_9.ppc64le/jre/lib/sunrsasign.jar:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.265.b01-1.el7_9.ppc64le/jre/lib/jsse.jar:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.265.b01-1.el7_9.ppc64le/jre/lib/jce.jar:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.265.b01-1.el7_9.ppc64le/jre/lib/charsets.jar:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.265.b01-1.el7_9.ppc64le/jre/lib/jfr.jar:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.265.b01-1.el7_9.ppc64le/jre/classes:/opt/appdynamics/java_agent/ver20.7.0.30639/javaagent.jar,wrapper,OpenJDK 64-Bit Server VM,UTF-8,executor,https://analytics-ingest.anypoint.mulesoft.com,TRUE,N/A,true,N/A,Java Virtual Machine Specification,N/A,http://java.oracle.com/,25538,N/A,OpenJDK Runtime Environment,10,acctapi-t102,sun.print.PSPrinterJob,237a436b6f0349c7870fe7c485d9c57f,8345d4bF6fE94C0FA474482078727AC8,/,:,com.singularity.ee.agent.log4j.CommonsLog4JFactoryAdapter,true,%MULE_LIB%:/opt/mule/acctapi-t102/conf:/opt/mule/acctapi-t102/lib/boot/commons-cli-1.2.jar:/opt/mule/acctapi-t102/lib/boot/commons-codec-1.11.jar:/opt/mule/acctapi-t102/lib/boot/disruptor-3.3.7.jar:/opt/mule/acctapi-t102/lib/boot/jackson-annotations-2.9.0.jar:/opt/mule/acctapi-t102/lib/boot/jackson-core-2.9.9.jar:/opt/mule/acctapi-t102/lib/boot/jackson-databind-2.9.9.jar:/opt/mule/acctapi-t102/lib/boot/jcl-over-slf4j-1.7.25.jar:/opt/mule/acctapi-t102/lib/boot/jul-to-slf4j-1.7.25.jar:/opt/mule/acctapi-t102/lib/boot/licm-2.1.4.jar:/opt/mule/acctapi-t102/lib/boot/log4j-1.2-api-2.11.0.jar:/opt/mule/acctapi-t102/lib/boot/log4j-api-2.11.0.jar:/opt/mule/acctapi-t102/lib/boot/log4j-core-2.11.0.jar:/opt/mule/acctapi-t102/lib/boot/log4j-slf4j-impl-2.11.0.jar:/opt/mule/acctapi-t102/lib/boot/mule-module-boot-ee-4.2.1.jar:/opt/mule/acctapi-t102/lib/boot/oscore-2.2.4.jar:/opt/mule/acctapi-t102/lib/boot/propertyset-1.3.jar:/opt/mule/acctapi-t102/lib/boot/slf4j-api-1.7.25.jar:/opt/mule/acctapi-t102/lib/boot/truelicense-1.29.jar:/opt/mule/acctapi-t102/lib/boot/truexml-1.29.jar:/opt/mule/acctapi-t102/lib/boot/wrapper-3.5.37.jar:/opt/appdynamics/java_agent/ver20.7.0.30639/javaagent.jar,3.5.37-st,1,1.8,"
    


