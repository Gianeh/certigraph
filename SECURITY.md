# Security policy

CertiGraph is a reference toolkit for verifiable graph computation. It is not yet a hardened security product.

## Supported versions

During the alpha phase, security fixes target the `main` branch and the latest tagged release.

## Reporting a vulnerability

Please open a private security advisory on GitHub, or contact the maintainers listed in the repository metadata.

High-priority issues include:

- a checker accepting an invalid certificate;
- malformed input causing uncontrolled crashes at documented API boundaries;
- certificate hashing or envelope bugs that make tampering undetectable;
- numerical tolerance behavior that can be exploited silently.

## Threat model

CertiGraph assumes producers may be untrusted. The checker is the trusted computing base. This means bugs in `certigraph/verify.py` are much more serious than bugs in `certigraph/produce.py`.

For adversarial deployments, prefer exact integer or rational data, pin checker versions, hash instances and certificates, and keep a signed audit log of accepted results.
