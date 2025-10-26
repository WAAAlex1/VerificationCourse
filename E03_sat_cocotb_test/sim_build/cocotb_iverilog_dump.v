module cocotb_iverilog_dump();
initial begin
    $dumpfile("/home/awa/VerificationCourse/E03_sat_cocotb_test/sim_build/sat_filter.fst");
    $dumpvars(0, sat_filter);
end
endmodule
