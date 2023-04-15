import React from 'react';

import Logo from "./images/vnit_logo.png"

function Title() {
    const mystyle={
        maxWidth: "540px",
    }
    return (
        <div className="card mb-3 mt-2 container border-0" style={{mystyle}}>
            <div className="row g-0">
                <div className="col-md-3">
                    <img src={Logo} alt="VNIT Logo" className="img-responsive margin-top" />
                </div>
                <div className="col-md-8 mt-4">
                    <div className="card-body">
                        <h1>Visvesvaraya National Institute of Technology</h1>
                        <h2>Nagpur</h2>
                    </div>
                </div>
            </div>
        </div>

    );
}

export default Title;