import React from 'react';

const HomePage = () => (
  <>
    <h1 className="mt-5">Sticky footer with fixed navbar</h1>
    <p className="lead">
      Pin a fixed-height footer to the bottom of the viewport in
      desktop browsers with this custom HTML and CSS. A fixed navbar has been added with
      <code>padding-top: 60px;</code>
      {' '}
      on the
      <code>body &gt; .container</code>
      .
    </p>
    <p>
      Back to
      <a href="../sticky-footer/">the default sticky footer</a>
      {' '}
      minus the navbar.
    </p>
  </>
);

export default HomePage;
