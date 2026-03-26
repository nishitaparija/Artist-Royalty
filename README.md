# 🎵 Artist Royalty — Blockchain-Based Music Royalty Distribution dApp

> A decentralised application (dApp) that eliminates intermediaries from music royalty distribution, ensuring artists are paid automatically, transparently, and fairly — every single play.

---

## 📌 Overview

The music industry has long suffered from opaque royalty systems where labels, distributors, and streaming platforms absorb the majority of an artist's earnings. **Artist Royalty** is a blockchain-based solution that puts control back in the hands of creators.
Artists upload their music directly on-chain. Every verified play triggers an automatic royalty payment via smart contract — no middlemen, no delays, no disputes.

---

## 🎬 Project Presentation

📊 **[View the full dApp walkthrough presentation on Canva](https://www.canva.com/design/DAHFDGIHUb8/V6O6gyWp1jDOCpLL3OW-QQ/view?utm_content=DAHFDGIHUb8&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hf64b992ab3)**

The presentation covers:
- The problem with traditional music royalty systems
- How the dApp works end-to-end
- Smart contract logic and royalty rules
- Security design decisions
- Tech stack overview
- Impact and future scope

---

## 🔧 How It Works

```
Artist uploads song
        │
        ▼
Song registered on-chain (immutable ownership record)
        │
        ▼
Play count tracked via verified on-chain events
        │
        ▼
Smart contract evaluates play threshold
        │
        ▼
Royalty payment automatically triggered to artist wallet
```

1. **Upload** — Artist registers their song on the blockchain with an immutable ownership record
2. **Track** — Play count is verified and recorded on-chain, preventing fraudulent inflation
3. **Pay** — Smart contract automatically distributes royalties proportional to verified plays
4. **Transparency** — All transactions are publicly visible on the decentralised ledger

---

## 🛡️ Security Design

Security was a first-class concern throughout development. The following vulnerabilities were considered and mitigated:

| Threat | Mitigation |
|---|---|
| Reentrancy attacks | Checks-Effects-Interactions pattern enforced |
| Play count fraud | On-chain verification logic, not client-side |
| Unauthorised withdrawals | Role-based access control on contract functions |
| Integer overflow | SafeMath / Solidity 0.8.x built-in overflow protection |
| Centralised failure points | Decentralised architecture eliminates single points of control |

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Smart Contracts | Solidity |
| Blockchain Network | Ethereum (local: Ganache) |
| Contract Deployment | Truffle |
| Frontend Interaction | Web3.js |
| Wallet Integration | MetaMask |
| Decentralised Storage | IPFS |
| Local Dev Blockchain | Ganache |

---

## 🚀 Getting Started

### Prerequisites

- Node.js & npm
- Truffle (`npm install -g truffle`)
- Ganache (local blockchain)
- MetaMask browser extension

### Installation

```bash
# Clone the repository
git clone https://github.com/nishitaparija/Artist-Royalty.git
cd Artist-Royalty

# Install dependencies
npm install

# Start local blockchain in Ganache
# Set port to 8545 in Ganache settings

# Compile and deploy contracts
truffle compile
truffle migrate --network development

# Launch the frontend
npm start
```

### Connect MetaMask

1. Open MetaMask and connect to your local Ganache network (`http://localhost:8545`)
2. Import one of the Ganache accounts using the provided private key
3. Interact with the dApp through the browser interface

---

## 📁 Project Structure

```
Artist-Royalty/
├── contracts/          # Solidity smart contracts
│   └── ArtistRoyalty.sol
├── migrations/         # Truffle deployment scripts
├── src/                # Frontend source files
│   ├── index.html
│   └── app.js          # Web3.js interaction layer
├── test/               # Smart contract unit tests
├── truffle-config.js   # Network configuration
└── README.md
```

---

## 🔮 Future Scope

- **NFT-based song ownership** — Tokenise songs as NFTs, enabling fans to co-own tracks and receive a share of royalties
- **Fan investment tokens** — Allow fans to buy tokens representing a stake in an artist's future earnings
- **Multi-chain deployment** — Extend to Polygon or Base for lower transaction fees
- **Streaming platform integration** — Oracle-based play count verification from real-world streaming data
- **DAO governance** — Let artists vote on platform parameters via decentralised governance

---

## ⚠️ Disclaimer
This project was developed for **educational purposes** as part of an engineering major project. Smart contracts have not been audited for production use. Do not deploy to mainnet without a full third-party security audit.

## 📜 License
This project is open source and available under the [MIT License](LICENSE).
